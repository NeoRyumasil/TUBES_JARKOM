import socket
import os

host = '127.0.0.1' 
port = 6789
def start_server():
    request = client_socket.recv(1024).decode()
    print(f"Request diterima:\n{request}")

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





if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Terhubung dengan {host}:{port}...")
    client_socket, addr = server_socket.accept()
    print(f"Terhubung dengan {addr}")
    start_server()
