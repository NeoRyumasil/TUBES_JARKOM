import socket
import os

def start_http_server():
    # Membuat socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'  # Bisa diganti sesuai kebutuhan
    port = 6789
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"HTTP Server listening on {host}:{port}...")

    # Menunggu dan menerima koneksi dari satu klien saja
    client_socket, addr = server_socket.accept()
    print(f"Terhubung dengan {addr}")

    request = client_socket.recv(1024).decode()
    print(f"Request diterima:\n{request}")

    # Parsing baris pertama dari HTTP request
    try:
        request_line = request.splitlines()[0]
        method, path, _ = request_line.split()
        filename = path.lstrip("/") or "index.html"  # Default: index.html

        if method != "GET":
            response = (
                "HTTP/1.1 405 Method Not Allowed\r\n"
                "Content-Type: text/plain\r\n\r\n"
                "405 Method Not Allowed"
            )
        elif not os.path.isfile(filename):
            response = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/plain\r\n\r\n"
                "404 Not Found: File tidak ditemukan"
            )
        else:
            with open(filename, "rb") as f:
                content = f.read()
            header = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(content)}\r\n\r\n"
            )
            client_socket.sendall(header.encode() + content)
            client_socket.close()
            return  # Keluar setelah melayani satu klien

    except Exception as e:
        print(f"Error parsing request: {e}")
        response = (
            "HTTP/1.1 400 Bad Request\r\n"
            "Content-Type: text/plain\r\n\r\n"
            "400 Bad Request"
        )

        client_socket.sendall(response.encode())
        client_socket.close()

    # Menutup server setelah melayani satu klien
    server_socket.close()

if __name__ == "__main__":
    start_http_server()
