import socket
import pickle
from random import random
import sys
import os


def send_with_chance(socket, data, dist):
    if random() > 0.3:
        socket.sendto(data, dist)


file_path = sys.argv[1]
if os.path.exists(file_path):
    os.remove(file_path)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("127.0.0.1", 41234))
last_accepted_package_number = None

while True:
    try:
        package, client = server_socket.recvfrom(1024)
        if package == b"eof":
            print("File successfully read and saved.")
            break
        data = pickle.loads(package)

        print(f"Recieved package number: {data["package_number"]}")
        if data["package_number"] == -1:
            print(data["data"])
            break

        if (
            last_accepted_package_number is None
            or last_accepted_package_number != data["package_number"]
        ):
            with open(file_path, "ab") as file:
                file.write(bytes(data["data"]))

        last_accepted_package_number = data["package_number"]

        send_with_chance(
            server_socket,
            pickle.dumps(
                {"package_number": last_accepted_package_number, "data": "ACK"}
            ),
            client,
        )

    except Exception as e:
        error = f"Internal server error: '{e}'."
        server_socket.sendto(
            pickle.dumps({"package_number": -1, "data": error}), client
        )
        print(error)
        break

server_socket.close()
