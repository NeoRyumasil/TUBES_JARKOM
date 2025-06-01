from socket import *
import sys

if len(sys.argv) <= 3:
    sys.exit()

namaServer = sys.argv[1]
portServer = int(sys.argv[2])
namaFile = sys.argv[3]

socketClient = socket(AF_INET, SOCK_STREAM)
socketClient.connect((namaServer, portServer))
print(f"Udah ke connect ke {namaServer}:{portServer} YAY")

request = f"GET /{namaFile} HTTP/1.1\r\nHost: {namaServer}\r\n\r\n"
socketClient.sendall(request.encode())

response = b""
while True:
    data = socketClient.recv(1024)
    if not data:
        break
    response += data

response = response.decode()
if "200 OK" in response:
    print("File ditemukan")
else:
    print("File tidak ditemukan")
    
print(f"Response dari server: {response}")

choice = input("Isi kata random untuk selesai: ")
if choice != "":
    print("Terima kasih telah menggunakan diri saya!")
    socketClient.close()