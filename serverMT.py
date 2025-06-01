import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 6789

# Handle client connections
def handle_client(client_socket, client_address):
    print(f"Connection established with {client_address}")
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received from {client_address}: {message}")
            client_socket.send(f"Echo: {message}".encode('utf-8'))
    except ConnectionResetError:
        print(f"Connection lost with {client_address}")
    finally:
        client_socket.close()
        print(f"Connection closed with {client_address}")

# Main server function
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server started on {HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()