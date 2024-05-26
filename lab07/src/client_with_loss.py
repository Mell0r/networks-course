import socket
from datetime import datetime
from random import random

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

client.settimeout(1.0)

server_address = ("127.0.0.1", 41234)

min_rtt: float | None = None
max_rtt: float | None = None
sum_rtt: float = 0
packets_lost = 0

for i in range(1, 11):
    print(f"Pinging {i}")
    sent_time = datetime.now()

    if random() < 0.2:
        print("Package 'lost'")
        packets_lost += 1
        continue

    client.sendto(f"Ping {i} {datetime.now()}".encode(), server_address)

    try:
        response, address = client.recvfrom(1024)
        rtt = (datetime.now() - sent_time).total_seconds()

        min_rtt = rtt if min_rtt is None else min(min_rtt, rtt)
        max_rtt = rtt if max_rtt is None else max(max_rtt, rtt)
        sum_rtt += rtt

        print(f"Got response: '{response.decode()}' in time {rtt}")
        print(f"Min rtt: {min_rtt}")
        print(f"Max rtt: {max_rtt}")
        print(f"Average rtt: {sum_rtt / i}")

    except socket.timeout:
        packets_lost += 1
        print("Request timed out")

print(f"Package loss: {packets_lost / 10 * 100}%")
client.close()
