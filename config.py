"""Configuration options to transmit by a client to the server."""

SETUP = {
    "sending": "dictionary",  # options: ['dictionary', 'file']
    "dictionary": {
        "USA": "Washington D.C.",
        "France": "Paris",
        "Ukraine": "Kyiv",
        "UK": "London",
    },
    "pickling_dict": "JSON",  # options: ['binary', 'JSON', 'XML']
    "encryption_file": True,
    "output": "screen",  # options: ['screen', 'file']
}
