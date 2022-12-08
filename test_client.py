"""Unit tests server module.

Run tests with the following command:
python -m pytest test_client.py -vv
"""

from server import transmit_content
from config import setup


def test_transmit_content():
    """Tests server.transmit_content function."""
    transmit_mode = "file"
    setup["output"] = transmit_mode
    content = "hola"
    transmit_content(content)
    with open("output.txt", "r") as in_file:
        actual_content = in_file.read()
    assert content == actual_content
