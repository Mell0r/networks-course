import socket
import pickle
import sys
from itertools import batched
from random import random


def send_with_chance(socket, data, dist):
    if random() > 0.3:
        socket.sendto(data, dist)


file_path = sys.argv[1]
timeout = float(sys.argv[2])

server = ("127.0.0.1", 41234)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(timeout)
package_number = 0

try:
    with open(file_path, "rb") as file:
        data_chunks = list(batched(file.read(), 200))
        ind = 0
        while ind < len(data_chunks):
            chunk = data_chunks[ind]
            data_encoded = pickle.dumps(
                {
                    "package_number": package_number,
                    "data": chunk,
                }
            )

            print(f"Sending package number: {package_number}")

            send_with_chance(
                client_socket,
                pickle.dumps(
                    {
                        "package_number": package_number,
                        "data": chunk,
                    }
                ),
                server,
            )
            try:
                data_encoded, _ = client_socket.recvfrom(1024)
                data = pickle.loads(data_encoded)
                if data["package_number"] == -1:
                    print(data["data"])
                    exit(-1)
                if data["package_number"] == package_number:
                    package_number = 1 - package_number
                    ind += 1
                    print("ACK received. Moving to next chunk...")
            except socket.timeout:
                print("Timeout. Resending chunk...")

    client_socket.sendto(b"eof", server)
    print("File successfully sent.")
except Exception as e:
    error = f"Internal client error: '{e}'."
    client_socket.sendto(
        pickle.dumps({"package_number": -1, "data": error.encode()}),
        server,
    )
    print(error)
