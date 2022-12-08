import json
import pickle
import socket

import xmltodict
from cryptography.fernet import Fernet

from config import setup

host = "127.0.0.1"
port = 9000
buffer = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
# set maximum accept rate to 5 connections"
s.listen(5)


def deserialize_dict(pick_format: str, dictionary):
    """Deserializes a binarized Python dictionary.""" 
    if pick_format == "binary":
        deserialized_data = pickle.loads(dictionary)
    elif pick_format == "JSON":
        deserialized_data = json.loads(dictionary)
    elif pick_format == "XML":
        xml_dict = xmltodict.parse(dictionary)
        deserialized_data = xml_dict["root"]
    return deserialized_data


def key_load(key_name):
    """Load a secret key for Fernet encryption/decryption."""
    with open(key_name, "rb") as my_key:
        key = my_key.read()
    return key


def decrypt_file(text_file):
    loaded_key = key_load("my_key.key")
    fernet = Fernet(loaded_key)
    with open(text_file, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # Decrypt data
    decrypted_data = fernet.decrypt(encrypted_data)

    # Write to the original file
    with open(text_file, "wb") as file:
        file.write(decrypted_data)


def receive_file(text_file):
    with open(text_file, "wb") as f:
        print("File opened")
        while True:
            bytes_read = client_socket.recv(buffer)
            if not bytes_read:
                break
            try:
                f.write(bytes_read)
            except Exception as e:  # e is the error message that could occur in the try block
                print(e)
    if setup["encryption_file"]:
        decrypt_file(text_file)


def transmit_content(content: str) -> None:
    """Transmits a string through either screen or a text file."""
    if setup["output"] == "screen":
        print(content)
    else:
        with open("output.txt", "w") as out_file:
            out_file.write(content)

# we need to include `if __name__ == '__main__':` because
# we cannot import functions implemented in this module
# from other Python modules without executing all the lines below
# unless we check that the global variable __name__ is different
# from the string '__main__'.

if __name__ == "__main__":
    while True:
        client_socket, address = s.accept()
        print("Connection from: " + str(address))
        if setup["sending"] == "dictionary":
            message = client_socket.recv(buffer)
            output_content = deserialize_dict(setup["pickling_dict"], message)
        else:
            receive_file("text_file.txt")
            with open("text_file.txt", "r") as f:
                output_content = f.read()
        transmit_content(output_content)
        # disconnect the server
        client_socket.close()
        break
    s.close()
