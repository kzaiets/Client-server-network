"""Unit tests client module

Run tests with the following command:
python -m pytest test_server.py -vv
"""

import pickle
import json
from dict2xml import dict2xml

from cryptography.fernet import Fernet

from client import (
    serialize_dict,
    encrypt_file,
)


def test_serialize_dict_binary():
    """Tests client.serialize_dict function."""
    pick_format_example = "binary"
    dictionary_example = {"a": 0, "b": 1}

    actual_serialized_dict = serialize_dict(
        pick_format=pick_format_example,
        dictionary=dictionary_example,
    )
    expected_serialized_dict = pickle.dumps(dictionary_example)
    assert actual_serialized_dict == expected_serialized_dict
    unexpected_serialized_dict = json.dumps(dictionary_example).encode()
    assert actual_serialized_dict != unexpected_serialized_dict


def test_serialize_dict_json():
    """Tests client.serialize_dict function."""
    pick_format_example = "json"  # 'JSON'
    dictionary_example = {"a": 0, "b": 1}

    actual_serialized_dict = serialize_dict(
        pick_format=pick_format_example,
        dictionary=dictionary_example,
    )
    expected_serialized_dict = pickle.dumps(dictionary_example)
    assert actual_serialized_dict != expected_serialized_dict
    unexpected_serialized_dict = json.dumps(dictionary_example).encode()
    assert actual_serialized_dict == unexpected_serialized_dict


def test_serialize_dict_xml():
    """Tests client.serialize_dict function."""
    pick_format_example = "xml"
    dictionary_example = {"a": 0, "b": 1}

    actual_serialized_dict = serialize_dict(
        pick_format=pick_format_example,
        dictionary=dictionary_example,
    )
    unexpected_serialized_dict = pickle.dumps(dictionary_example)
    assert actual_serialized_dict != unexpected_serialized_dict
    unexpected_serialized_dict = json.dumps(dictionary_example).encode()
    assert actual_serialized_dict != unexpected_serialized_dict
    expected_serialized_dict = dict2xml(
        dictionary_example, wrap="root", indent=""
    ).encode()
    assert actual_serialized_dict == expected_serialized_dict


def test_encrypt_file(tmp_path):
    """Tests client.encrypt_file function."""
    d = tmp_path / "sub"
    d.mkdir()
    text_path = tmp_path / "hello.txt"
    text_path.write_text("hola")
    encrypted_text = encrypt_file(text_path)
    with open("my_key.key", "rb") as my_key:
        loaded_key = my_key.read()
    fernet = Fernet(loaded_key)
    actual_decrypted_text = fernet.decrypt(encrypted_text)
    expected_decrypted_text = b"hola"

    assert encrypted_text != "hola"
    assert actual_decrypted_text == expected_decrypted_text
