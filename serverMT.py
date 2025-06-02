import socket
import os
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 6789

# Get content type based on file extension
def get_content_type(filename):
    if filename.endswith(".html") or filename.endswith(".htm"):
        return "text/html"
    elif filename.endswith(".css"):
        return "text/css"
    elif filename.endswith(".js"):
        return "application/javascript"
    elif filename.endswith(".png"):
        return "image/png"
    elif filename.endswith(".jpg") or filename.endswith(".jpeg"):
        return "image/jpeg"
    else:
        return "application/octet-stream"

# Handle client connections
def handle_client(client_socket, client_address):
    try:
        request = client_socket.recv(1024).decode()
        print(f"Request received from {client_address}:\n{request}")

        lines = request.splitlines()
        if len(lines) == 0:
            client_socket.close()
            return

        # Parse request line, example: GET /index.html HTTP/1.1
        request_line = lines[0]
        parts = request_line.split()
        if len(parts) < 2:
            client_socket.close()
            return

        filename = parts[1].lstrip('/').replace(",", ".")  # Fix typo: index,html -> index.html
        if filename == '':
            filename = 'index.html'

        if os.path.isfile(filename):
            with open(filename, 'rb') as f:
                body = f.read()
            content_type = get_content_type(filename)
            header = (
                "HTTP/1.1 200 OK\r\n"
                f"Content-Type: {content_type}\r\n"
                f"Content-Length: {len(body)}\r\n\r\n"
            )
            response = header.encode() + body
            client_socket.sendall(response)
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
    finally:
        client_socket.close()

# Main server function
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
