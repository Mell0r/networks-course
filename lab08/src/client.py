import socket
import sys
import os

from shared import send_file, recieve_file

send_file_path = sys.argv[1]
recieve_file_path = sys.argv[2]
timeout = float(sys.argv[3])

if os.path.exists(recieve_file_path):
    os.remove(recieve_file_path)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Sending...\n")

send_file(client_socket, send_file_path, timeout, ("127.0.0.1", 41234))

print("\nRecieving...\n")

recieve_file(client_socket, recieve_file_path)
