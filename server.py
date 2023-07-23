import socket
import threading

def handle_client(client_socket, address):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print(f"Connection closed with {address}")
                break
            print(f"Received message from {address}: {message}")
            # Broadcast the message to all connected clients
            broadcast(message, client_socket)
        except Exception as e:
            print(f"Error: {e}")
            break

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error broadcasting message: {e}")

HOST = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print("Chat server started.")

clients = []

while True:
    client_socket, address = server.accept()
    print(f"Connected with {address}")
    clients.append(client_socket)
    client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
    client_handler.start()
