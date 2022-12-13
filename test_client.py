"""Unit tests client module

Run tests with the following command:
python -m unittest test_server.py -v
"""

import json
import pickle
import tempfile
import unittest
from pathlib import Path

from cryptography.fernet import Fernet
from dict2xml import dict2xml

from client import encrypt_file, serialize_dict


class TestClient(unittest.TestCase):
    """Test suite for the client module."""

    def serialize_dict(self):
        """Tests client.serialize_dict with different encodings."""
        dictionary_example = {"a": 0, "b": 1}
        # binary
        serialized_dict_b = serialize_dict("binary", dictionary_example)
        expected_serialized_dict_b = pickle.dumps(dictionary_example)
        self.assertEqual(serialized_dict_b, expected_serialized_dict_b)
        # json
        serialized_dict_json = serialize_dict("JSON", dictionary_example)
        expected_serialized_dict_json = pickle.dumps(dictionary_example)
        self.assertEqual(serialized_dict_json, expected_serialized_dict_json)
        # xml
        serialized_dict_xml = serialize_dict("XML", dictionary_example)
        expected_serialized_dict_xml = dict2xml(
            dictionary_example, wrap="root", indent=""
        ).encode()
        self.assertEqual(serialized_dict_xml, expected_serialized_dict_xml)

    def test_encrypt_file(self):
        """Tests client.encrypt_file function."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_subdir = Path(temp_dir, "sub")
            temp_subdir.mkdir()
            text_path = temp_subdir / "hello.txt"
            text_path.write_text("hola")
            encrypted_text = encrypt_file(text_path)
            with open("my_key.key", "rb") as my_key:
                loaded_key = my_key.read()
            fernet = Fernet(loaded_key)
            actual_decrypted_text = fernet.decrypt(encrypted_text)
            expected_decrypted_text = b"hola"

            self.assertTrue(encrypted_text != "hola")
            self.assertTrue(actual_decrypted_text == expected_decrypted_text)




