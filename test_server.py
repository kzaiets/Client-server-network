"""Unit tests server module.

Run tests with the following command:
python -m unittest test_client.py -v
"""

import unittest

from config import SETUP
from server import output


class TestServer(unittest.TestCase):
    """Test suite for the server module."""

    def test_output(self):
        """Tests server.transmit_content in a simple setting."""
        output_mode = "file"
        SETUP["output"] = output_mode
        content = "hola"
        output(content)
        with open("output.txt", "r") as in_file:
            actual_content = in_file.read()
        self.assertTrue(content == actual_content)

