"""Client module"""

import json
import pickle
import socket

from cryptography.fernet import Fernet
from dict2xml import dict2xml

from config import SETUP
from server import HOST, PORT, BUFFER

# instance of Fernet class created and key generated
key = Fernet.generate_key()
fernet = Fernet(key)
with open("my_key.key", "wb") as my_key:
    my_key.write(key)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def serialize_dict(pickling_format: str, dictionary: dict) -> bytes:
    """Serializes a dictionary depending on the choice of the pickling format.

    Args:
        pickling_format (str): ['binary', 'JSON', 'XML'] pickling format to use.
        dictionary (dict): a Python dictionary.

    Returns:
        bytes: the Python dictinary serialized in the chosen pickling format.
    """
    if pickling_format == "binary":
        serialized_data = pickle.dumps(dictionary)
    elif pickling_format == "JSON":
        serialized_data = json.dumps(dictionary).encode()
    elif pickling_format == "XML":
        serialized_data = dict2xml(dictionary, wrap="root", indent="").encode()
    return serialized_data


def encrypt_file(text_path: str) -> bytes:
    """Opens and encrypts the content of the given file.

    Args:
        text_path (str): a path to a text file.

    Returns:
        bytes: encrypted content of the given text file.
    """
    with open(text_path, "rb") as f_orig:
        original_file = f_orig.read()
    encrypted = fernet.encrypt(original_file)
    with open(text_path, "wb") as f_encrypted:
        f_encrypted.write(encrypted)
    return encrypted


def send_file(text_path: str) -> None:
    """Sends a file to the server.

    Args:
        text_file (str): a path to a text file.
    """
    try:
        if SETUP["encryption_file"]:
            encrypt_file(text_path)
        with open(text_path, "rb") as in_file:
            print(in_file)
            while True:
                file_read = in_file.read(BUFFER)
                if not file_read:
                    break  # file transmitting is done
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
        s.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("There is a problem with the connection.")
    if SETUP["sending"] == "dictionary":
        output_data = serialize_dict(
            SETUP["pickling_dict"], SETUP["dictionary"]
        )
        s.send(output_data)
    else:
        send_file("text_file.txt")
