"""Server module"""

import json
import pickle
import socket

import xmltodict
from cryptography.fernet import Fernet

from config import SETUP_DICT

# source: https://peps.python.org/pep-0008/#constants
HOST: str = "127.0.0.1"
PORT: int = 9000
BUFFER: int = 1024


def deserialize_dict(pickling_format: str, dictionary: bytes) -> dict:
    """Deserializes a binarized Python dictionary.

    Args:
        pickling_format (str): ['binary', 'JSON', 'XML'] pickling format to use.
        dictionary (dict): a serialized Python dictionary.

    Returns:
        dict: the Python dictinary deserialized in the chosen pickling format.
    """
    if pickling_format == "binary":
        deserialized_data = pickle.loads(dictionary)
    elif pickling_format == "JSON":
        deserialized_data = json.loads(dictionary)
    elif pickling_format == "XML":
        xml_dict = xmltodict.parse(dictionary)
        deserialized_data = xml_dict["root"]
    return deserialized_data


def key_load(key_name: str) -> bytes:
    """Loads a secret key for Fernet encryption/decryption."""
    with open(key_name, "rb") as my_key:
        key = my_key.read()
    return key


def decrypt_file(text_path: str) -> None:
    """Decrypts a text file that has been encrypted with Fernet.

    Args:
        text_path (str): a path to a text file.
    """
    loaded_key = key_load("my_key.key")
    fernet = Fernet(loaded_key)
    with open(text_path, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()  # read the encrypted data
    decrypted_data = fernet.decrypt(encrypted_data)  # decrypt data

    # Write to the original file
    with open(text_path, "wb") as file:
        file.write(decrypted_data)


def receive_file(text_path: str) -> None:
    """Receives and decrypts a text file"""
    with open(text_path, "wb") as in_file:
        print("File opened")
        while True:
            bytes_read = client_socket.recv(BUFFER)
            if not bytes_read:
                break
            try:
                in_file.write(bytes_read)
            # `exception` is the error message that could occur in the try block
            except Exception as exception:
                print(exception)
    if SETUP_DICT["encryption_file"]:
        decrypt_file(text_path)


def output(content) -> None:
    """Transmits a string through either screen or a text file."""
    if SETUP_DICT["output"] == "screen":
        print(content)
    elif SETUP_DICT["output"] == "file":
        with open("output.txt", "w") as out_file:
            out_file.write(content)


# we need to include `if __name__ == '__main__':` because
# we cannot import functions implemented in this module
# from other Python modules without executing all the lines below
# unless we check that the global variable __name__ is different
# from the string '__main__'.

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)  # set maximum accept rate to 5 connections"

    while True:
        client_socket, address = s.accept()
        print("Connection from: " + str(address))
        if SETUP_DICT["sending"] == "dictionary":
            message = client_socket.recv(BUFFER)
            output_content = deserialize_dict(SETUP_DICT["pickling_dict"], message)
        else:
            receive_file("text_file.txt")
            with open("text_file.txt", "r") as f:
                output_content = f.read()
        output(output_content)
        # disconnect the server
        client_socket.close()
        break
    s.close()
