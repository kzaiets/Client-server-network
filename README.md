# Client-Server Network - Group Project

## Description
This project was developed by Karina, Alice and Flaviano as a deliverable for the CSCK541 Software Development in Practice October 2022B class that is a requirement to complete a MSc. in Data Science and Artificial Intelligence by the University of Liverpool.  
A simple client/server network had to be implemented, and once it was done it had to be able to perform a series of tasks detailed in the USAGE section below.

## Data
The possible format that a client can transmit to the server (and that the server can handle) are the following:
- text file
- Python dictionary

## Install
Clone the repo:
```bash
git clone https://github.com/kzaiets/Client-server-network.git
```

Install the requirements:
```bash
pip install -r requirements.txt
```

# Usage

First of all, run the server:
```bash
python server.py
```

Then, run the client:
```bash
python client.py
```

This basic client/server network allows the following usage:
a. Create a dictionary, populate it, serialize it and send it to a server
b. Create a text file and send it to a server

For the dictionary, the user is able to set the pickling format to one of the following: binary, JSON and XML. The user is also offered the option to encrypt the text in a text file.

The server allows you to send the content to a screen or to a file. The server is also able to handle encrypted contents. The client and the server are implemented in the same machine.

## Unit tests
The proposed unit tests checks the following functionalities:
1. Creation of a dictionary, populate it, serialize and send it to a server
2. It test the following pickling format: binary, JSON and XML
3. Creation of a text file and send it to the server
4. The encrypt function is tested showing the message, the encrypted message and the original message once decrypted.

To run the unit tests for the client:
```bash
python -m unittest test_client.py -v
```

To run the unit tests for the server:
```bash
python -m unittest test_server.py -v
```

## License
MIT License

## Authors
Karina Zaiets: Software Engineer and Software Architect
Alice Chui: Project Manager and Software Architect
Flavino Moreira: Tester and Software Architect

