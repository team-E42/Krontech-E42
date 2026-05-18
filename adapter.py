import socket
import websockets
import asyncio
import random

clients = set()

async def wshandler(websocket):
    clients.add(websocket)

    print("Browser connected")
    
    try:
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)
        print("Browser disconnected")

async def send_to_browsers(message):
    if clients:
        await asyncio.gather(*(client.send(message) for client in clients))

async def tcp_loop():
    host = "127.0.0.1" #"10.179.221.238"
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
        await send_to_browsers(f"{' '.join(lf)} {letter}")

async def main():
    await websockets.serve(wshandler, "localhost", 4040)

    print("WebSocket server started on ws://localhost:4040")

    await tcp_loop()

asyncio.run(main())
        
