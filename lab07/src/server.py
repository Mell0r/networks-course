import socket
import random

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("127.0.0.1", 41234))

while True:
    data, address = server.recvfrom(1024)
    if random.random() > 0.2:
        server.sendto(data.decode().upper().encode(), address)
