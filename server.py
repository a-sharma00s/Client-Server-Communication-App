'''
File: server.py
Authors: Ashish Sharma, Hamza Siddiqui
Date: 10/01/2024
About: server for communication application allowing for chatting between client and server
'''

# server.py
import socket
import datetime

# Create a TCP socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to IP address and port
serverIP = '192.168.2.52'
serverPort = 51538 
serverSocket.bind((serverIP, serverPort))

# listen to max 3 devices at a time
serverSocket.listen(3)

# Look for connections
serverSocket.listen(3)
print(f"Server is listening on {serverIP}:{serverPort}")

client_cache = {}
client_count = 0

while True:
    # Accept client connection
    client_socket, client_address = serverSocket.accept()
    print(f"Connection established with {client_address}")

    # Assign client name
    client_name = f"Client{client_count:02d}"
    client_count += 1
    
    if client_count > 4:
        print(f"Client number exceeded. Disconnecting server.")
        break

    # Record connection time
    connect_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # add client info cache
    client_cache[client_name] = {
        "address": client_address,
        "connected_at": connect_time,
        "disconnected_at": None
    }

    # Send message back to the client
    client_socket.send(f"Hello {client_name}, welcome to the server!".encode('utf-8'))

    while True:
        # Receive message from the client
        data = client_socket.recv(1024)
        if not data:
            print(f"Client {client_name} disconnected.")
            break
        message = data.decode('utf-8')
        print(f"Received from {client_name}: {message}")

        if message.lower() == "status":
            status_message = "\n".join([f"{name}: connected_at={info['connected_at']}, disconnected_at={info['disconnected_at']}"
                                        for name, info in client_cache.items()])
            client_socket.send(status_message.encode('utf-8'))

        elif message.lower() == "exit":
            print(f"{client_name} is disconnecting")
        
        # Echo the message back with "ACK" appended
        returnMessage = message + " ACK"
        client_socket.send(returnMessage.encode('utf-8'))

    # Close the client connection
    client_socket.close()