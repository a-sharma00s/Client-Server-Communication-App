'''
File: client.py
Authors: Ashish Sharma, Hamza Siddiqui
Date: 10/01/2024
About: Client for communication application allowing for chatting between client and server
'''
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Server address and port
serverIP = '192.168.2.52'
serverPort = 51538

#Connect to server
client_socket.connect((serverIP, serverPort))
print(f"Connected to the server at {serverIP}:{serverPort}")

#Get server welcome message
welcomeMessage = client_socket.recv(1024).decode('utf-8')
print(f"Server: {welcomeMessage}")

while True:
    #User input
    message = input("Enter a message (Type 'exit' to disconnect from server)")
    if message.lower() == "exit":
        print(f"Disconnecting from the server")
        break

    #Message to server
    client_socket.send(message.encode('utf-8'))

    #Message from server
    serverResponse = client_socket.recv(1024).decode('utf-8')
    print(f"Server response: {serverResponse}")

#Close connection
client_socket.close()