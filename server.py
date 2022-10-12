import threading
import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 65432
SERVER_ADDRESS = (HOST, PORT)
DEFAULT_STRING_FORMAT = "utf-8"
MESSAGE_LENGTH_HEADER_LENGTH = 128

clients = []

def handle_new_client(connection: socket.socket, address):
    clients.append(connection)
    
    while True:
        initial_header = connection.recv(MESSAGE_LENGTH_HEADER_LENGTH).decode(DEFAULT_STRING_FORMAT)
        if initial_header:
            message_length = int(initial_header)
            message = connection.recv(message_length).decode(DEFAULT_STRING_FORMAT)
            
            message = f"{address} - {message}".encode(DEFAULT_STRING_FORMAT)
            message_length = ("0"*(MESSAGE_LENGTH_HEADER_LENGTH - len(str(len(message)))) + str(len(message))).encode(DEFAULT_STRING_FORMAT)
            for client in clients:
                # Here, the idea is to spread the message to all other clients, but first we have to send
                # the length of the message that's coming
                if client != connection:
                    client.sendall(message_length)
                    client.sendall(message)
        else:
            break

    clients.remove(connection)

def handle_init():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(SERVER_ADDRESS)
    server.listen()

    while True:
        connection, address = server.accept()
        threading.Thread(target=handle_new_client, args=[connection,address]).start()
        print(f"[*] New connection! Say hello to {address}")


if __name__ == "__main__":
    handle_init()
