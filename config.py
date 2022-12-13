"""Configuration options to transmit by a client to the server."""

SETUP = {
    "sending": "file",  # options: ['dictionary', 'file']
    "dictionary": {
        "USA": "Washington D.C.",
        "France": "Paris",
        "Ukraine": "Kyiv",
        "UK": "London",
    },
    "pickling_dict": "JSON",  # options: ['binary', 'JSON', 'XML']
    "encryption_file": True, # options: True/False
    "output": "screen",  # options: ['screen', 'file']
}
