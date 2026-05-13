import socket

host = "192.168.100.111"
port = 8080

server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(1)

conn, address = server_socket.accept() 
print(f"Connection from: {address}")
while True:
    data = conn.recv(1024).decode()
    if not data: break
    print(f"Data from glove: {data}")
    
