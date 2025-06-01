import socket
import os
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 6789

# Handle client connections
def handle_client(client_socket, client_address):
    request = client_socket.recv(1024).decode()
    print(f"Request received from {client_address}:\n{request}")

    lines = request.splitlines()
    if  len(lines) == 0:
        client_socket.close()
        return

    filename = lines[0].split()[1].lstrip('/')
    if filename == '':
        filename = 'index.html'
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            body = f.read() 
        header = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(body)}\r\n\r\n"
        )   
        response = header.encode() + body
    else:
        body = """
            <html>
                <head><title>404 Not Found</title></head>
                <body>
                    <h1>404 Not Found</h1>
                    <p>File not found</p>
                </body>
            </html>
        """
        client_socket.sendall(
            f"HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(body)}\r\n\r\n".encode() + body.encode()
        )
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