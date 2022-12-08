import json
import pickle
import socket

from cryptography.fernet import Fernet
from dict2xml import dict2xml

from config import setup

# instance of Fernet class created and key generated
key = Fernet.generate_key()
fernet = Fernet(key)
with open("my_key.key", "wb") as my_key:
    my_key.write(key)

host = "127.0.0.1"
port = 9000
buffer = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def serialize_dict(pick_format, dictionary):
    """depending on the choice of the pickling format, the dictionary is serialised"""
    lower_pick_format = pick_format.lower()
    if lower_pick_format == "binary":
        serialized_data = pickle.dumps(dictionary)
    elif lower_pick_format == "json":
        serialized_data = json.dumps(dictionary).encode()
    elif lower_pick_format == "xml":
        serialized_data = dict2xml(dictionary, wrap="root", indent="").encode()
    else:
        NotImplementedError(f"{pick_format} not implemented.")
    return serialized_data


def encrypt_file(text_file):
    with open(text_file, "rb") as f_orig:
        original_file = f_orig.read()
    encrypted = fernet.encrypt(original_file)
    with open(text_file, "wb") as f_encrypted:
        f_encrypted.write(encrypted)
    return encrypted


def send_file(text_file):
    try:
        if setup["encryption_file"]:
            encrypt_file(text_file)
        with open(text_file, "rb") as f:
            print(f)
            while True:
                file_read = f.read(buffer)
                if not file_read:
                    # file transmitting is done
                    break
                # use sendall to assure transmission in busy networks
                s.sendall(file_read)
        print("Successfully sent the file")
    except TypeError:
        print("There was a problem sending the file.")


# we need to include `if __name__ == '__main__':` because
# we cannot import functions implemented in this module
# from other Python modules without executing all the lines below
# unless we check that the global variable __name__ is different
# from the string '__main__'.

if __name__ == "__main__":
    try:
        s.connect((host, port))
    except ConnectionRefusedError:
        print("There is a problem with the connection.")
    if setup["sending"] == "dictionary":
        output_data = serialize_dict(setup["pickling_dict"], setup["dictionary"])
        s.send(output_data)
    else:
        send_file("text_file.txt")
