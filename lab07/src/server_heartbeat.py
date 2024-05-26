import socket
import random
from datetime import datetime
from typing import Dict
import sys


def check_clients(
    last_client_package: Dict[tuple[str, int], tuple[int, datetime]],
    client_timeout: float,
):
    for client, pckg in last_client_package.items():
        if (datetime.now() - pckg[1]).total_seconds() > client_timeout:
            print(f"Client {client} seems to be stopped.")

    last_client_package = {
        client: pckg
        for client, pckg in last_client_package.items()
        if (datetime.now() - pckg[1]).total_seconds() < client_timeout
    }


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("127.0.0.1", 41234))

last_client_package: Dict[tuple[str, int], tuple[int, datetime]] = {}

client_timeout = float(sys.argv[1])
server_socket.settimeout(client_timeout)

while True:
    try:
        data, client = server_socket.recvfrom(1024)
        message = data.decode()
        print(f"Got message '{message}' from {client}.")

        package_number = int(message.split()[1])
        current_timestamp = datetime.strptime(
            message.split()[2] + " " + message.split()[3], "%Y-%m-%d %H:%M:%S.%f"
        )

        prev_package = last_client_package.get(client)
        if prev_package is not None:
            package_dist = package_number - prev_package[0]
            if package_dist > 1:
                print(f"Lost {package_dist - 1} package(-s) from client {client}")

        last_client_package[client] = (package_number, current_timestamp)

        if random.random() > 0.2:
            server_socket.sendto(data.decode().upper().encode(), client)

        check_clients(last_client_package, client_timeout)

    except socket.timeout:
        for client in last_client_package:
            print(f"Client {client} seems to be stopped.")
        last_client_package = {}
