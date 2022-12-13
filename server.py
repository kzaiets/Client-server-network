import socket
import pickle
import json
import xmltodict
from cryptography.fernet import Fernet
import logging
from config import setup

# logging setup
log_format = f"%(levelname)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_format)
logger = logging.getLogger(__name__)

# file setup
output_file = "output.txt"
file_received = "text_file.txt"
key_file = 'my_key.key'

# socket setup
host = '127.0.0.1'
port = 9000
buffer = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
# set maximum accept rate to 5 connections"
s.listen(5)


def deserialize_dict(pick_format, dictionary):
    if pick_format == 'binary':
        deserialized_data = pickle.loads(dictionary)
    elif pick_format == 'JSON':
        deserialized_data = json.loads(dictionary)
    elif pick_format == 'XML':
        xml_dict = xmltodict.parse(dictionary)
        deserialized_data = xml_dict["root"]
    return deserialized_data


def key_load(key_name):
    with open(key_name, 'rb') as my_key:
        key = my_key.read()
    return key


def decrypt_file(text_file):
    loaded_key = key_load(key_file)
    fernet = Fernet(loaded_key)
    with open(text_file, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # Decrypt data
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    except Fernet.InvalidToken as e:
        logger.warning("Can't decrypt the file, invalid token or value")
        decrypted_data = None

    # Write to the original file
    with open(text_file, "wb") as file:
        file.write(decrypted_data)


def receive_file(text_file):
    with open(text_file, "wb") as f:
        while True:
            bytes_read = client_socket.recv(buffer)
            if not bytes_read:
                break
            try:
                f.write(bytes_read)
            except TypeError:
                logger.warning("TypeError occurred")
    if setup['encryption_file']:
        decrypt_file(text_file)


def output(contents):
    if setup['output'] == 'screen':
        print(contents)
    else:
        with open(output_file, 'w') as f:
            f.write(str(contents))


client_socket, address = s.accept()
logger.debug("Connection from: " + str(address))
if setup['sending'] == 'dictionary':
    message = client_socket.recv(buffer)
    output_content = deserialize_dict(setup['pickling_dict'], message)
else:
    receive_file(file_received)
    with open(file_received, 'r') as f:
        output_content = f.read()
output(output_content)
s.close()




