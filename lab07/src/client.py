import socket
from datetime import datetime

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

client.settimeout(1.0)

server_address = ("127.0.0.1", 41234)

packets_lost = 0

for i in range(1, 11):
    print(f"Pinging {i}")
    sent_time = datetime.now()
    client.sendto(f"Ping {i} {datetime.now()}".encode(), server_address)

    try:
        response, address = client.recvfrom(1024)
        rtt = (datetime.now() - sent_time).total_seconds()
        print(f"Got response: '{response.decode()}' in time {rtt}")

    except socket.timeout:
        packets_lost += 1
        print("Request timed out")

client.close()
