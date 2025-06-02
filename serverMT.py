import socket
import os
import threading

HOST = '127.0.0.1'
PORT = 6789
def handle_client(client_socket, addr):
    request = client_socket.recv(1024).decode()
    print(f"Request diterima dari {addr}:\n{request}")

    request_line = request.splitlines()[0]
    method, path, _ = request_line.split()
    filename = path.lstrip("/")
    
    if not os.path.isfile(filename):
        body = """
            <html>
                <head><title>404 Not Found</title></head>
                <body>
                    <h1>404 Not Found</h1>
                    <p>File tidak ditemukan</p>
                </body>
            </html>
        """
        header = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(body)}\r\n\r\n"
        )
        client_socket.sendall(header.encode() + body.encode())
    else:
        with open(filename, "rb") as f:
            body = f.read()
        header = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(body)}\r\n\r\n"
        )
        client_socket.sendall(header.encode() + body)
    client_socket.close()

# Main server function
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server started on {HOST}:{PORT}")

    try:
        while True:
            client_socket, addr = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
