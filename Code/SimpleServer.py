import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 8000))
print("Socket bound to " + sock.getsockname()[0])
sock.listen()
print("Server listening...")

while True:
    connectionSocket, addr = sock.accept()
    print("CONNECTED SOURCE: " + str(addr))
    connectionSocket.close()