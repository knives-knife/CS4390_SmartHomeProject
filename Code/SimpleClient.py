import socket
import time

# Default IP Address for h1 being the server
serverAddr = "10.0.0.1"

clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Attempting connection to " + serverAddr)
clientSock.connect((serverAddr, 8000))
time.sleep(1)
print("Closing connection and exiting...")
clientSock.close()
