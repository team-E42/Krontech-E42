import socket

host = "10.179.221.238"
port = 8080

server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(1)

conn, address = server_socket.accept() 
print(f"Connection from: {address}")

file = open("./mlmodel/data/train.txt", "a")

df = []

while True:
    data = conn.recv(1024).decode()
    if not data: break
    for item in data.split("\r\n"):
        df.append(item)

    lf = []
    for item in df:
        if item == "$" and lf != []:
            df = []
            break
        elif item == "$": 
            continue
        else: lf.append(item)
    if len(lf) != 5:
        continue

    print(" ".join(lf))
    letter = input(">")
    if letter == "":
        continue
    print(f"{' '.join(lf)} {letter}", file=file)    
        
