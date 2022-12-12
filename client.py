import socket
import pickle
import json
from cryptography.fernet import Fernet
from dict2xml import dict2xml
from config import setup

# instance of Fernet class created and key generated
key = Fernet.generate_key()
fernet = Fernet(key)
with open('my_key.key', 'wb') as my_key:
    my_key.write(key)

host = '127.0.0.1'
port = 9000
buffer = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def serialize_dict(pick_format, dictionary):
    """depending on the choice of the pickling format, the dictionary is serialised"""
    if pick_format == 'binary':
        serialized_data = pickle.dumps(dictionary)
    elif pick_format == 'JSON':
        serialized_data = json.dumps(dictionary).encode()
    elif pick_format == 'XML':
        serialized_data = dict2xml(dictionary, wrap='root', indent="").encode()
        print(serialized_data)
    return serialized_data


def encrypt_file(text_file):
    with open(text_file, 'rb') as f_orig:
        original_file = f_orig.read()
    encrypted = fernet.encrypt(original_file)
    with open(text_file, 'wb') as f_encrypted:
        f_encrypted.write(encrypted)
    return encrypted


def send_file(text_file):
    try:
        if setup['encryption_file']:
            encrypt_file(text_file)
        with open(text_file, "rb") as f:
            print(f)
            while True:
                file_read = f.read(buffer)
                print(file_read)
                if not file_read:
                    # file transmitting is done
                    break
                # use sendall to assure transmission in busy networks
                s.sendall(file_read)
        print('Successfully sent the file')
    except TypeError as e:
        print(e)
        print("There was a problem sending the file.")


try:
    s.connect((host, port))
except ConnectionRefusedError:
    print("There is a problem with the connection.")

try:
    if setup['sending'] == 'dictionary':
        output_data = serialize_dict(setup['pickling_dict'], setup['dictionary'])
        s.send(output_data)
    else:
        send_file("text_file.txt")
except BrokenPipeError as e:
    print('Run the server file first!')





