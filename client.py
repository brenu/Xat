import socket
import threading
from unittest.mock import DEFAULT

HOST = socket.gethostbyname(socket.gethostname())
PORT = 65432
SERVER_ADDRESS = (HOST, PORT)
DEFAULT_STRING_FORMAT = "utf-8"
MESSAGE_LENGTH_HEADER_LENGTH = 128

def handle_input(client: socket.socket):
    while True:
        message = input().encode(DEFAULT_STRING_FORMAT)
        message_length = ("0"*(MESSAGE_LENGTH_HEADER_LENGTH - len(str(len(message)))) + str(len(message))).encode(DEFAULT_STRING_FORMAT)
        client.sendall(message_length)
        client.sendall(message)


def handle_init():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(SERVER_ADDRESS)

    threading.Thread(target=handle_input, args=[client]).start()
    while True:
        initial_packet = client.recv(MESSAGE_LENGTH_HEADER_LENGTH).decode(DEFAULT_STRING_FORMAT)

        if initial_packet:
            incoming_message_length = int(initial_packet)

            message = client.recv(incoming_message_length).decode(DEFAULT_STRING_FORMAT)
            print(message)

if __name__ == "__main__":
    handle_init()