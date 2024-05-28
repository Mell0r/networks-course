import socket
import sys
import os

from shared import recieve_file, send_file

send_file_path = sys.argv[1]
recieve_file_path = sys.argv[2]
timeout = float(sys.argv[3])

if os.path.exists(recieve_file_path):
    os.remove(recieve_file_path)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("127.0.0.1", 41234))

print("Recieving...\n")

client_address = recieve_file(server_socket, recieve_file_path)

print("\nSending...\n")

if client_address is not None:
    send_file(server_socket, send_file_path, timeout, client_address)

server_socket.close()
