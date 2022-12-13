"""Server module"""

import json
import pickle
import socket
import xmltodict
import cryptography
from cryptography.fernet import Fernet
import logging
from config import SETUP

# socket setup
# source: https://peps.python.org/pep-0008/#constants
HOST = "127.0.0.1"
PORT = 9000
BUFFER = 1024


# logging setup
log_format = f"%(levelname)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_format)
logger = logging.getLogger(__name__)

# file setup
output_file = "output.txt"
file_received = "text_file.txt"
key_file = 'my_key.key'


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
    loaded_key = key_load(key_file)
    fernet = Fernet(loaded_key)
    with open(text_path, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # Decrypt data
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    except cryptography.fernet.InvalidToken:
        logger.warning("Can't decrypt the file, invalid token or value")
        decrypted_data = None
    # Write to the original file
    with open(text_path, "wb") as file:
        file.write(decrypted_data)

            
def receive_file(text_path: str) -> None:
    """Receives and decrypts a text file"""
    with open(text_path, "wb") as in_file:
        while True:
            bytes_read = client_socket.recv(BUFFER)
            if not bytes_read:
                break
            try:
                in_file.write(bytes_read)
            except TypeError:
                logger.warning("TypeError occurred")
    if SETUP['encryption_file']:
        decrypt_file(text_path)


def output(content) -> None:
    """Transmits a string through either screen or a text file."""
    if SETUP["output"] == "screen":
        print(content)
    elif SETUP["output"] == "file":
        with open(output_file, "w") as out_file:
            out_file.write(str(content))


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)  # set maximum accept rate to 5 connections"
    client_socket, address = s.accept()
    logger.debug("Connection from: " + str(address))
    if SETUP['sending'] == 'dictionary':
        message = client_socket.recv(BUFFER)
        output_content = deserialize_dict(SETUP['pickling_dict'], message)
    else:
        receive_file(file_received)
        with open(file_received, 'r') as f:
            output_content = f.read()
    output(output_content)
    s.close()




