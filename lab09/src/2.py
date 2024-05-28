import socket
from sys import argv

ip = argv[1]
from_scoket = int(argv[2])
to_scoket = int(argv[3])

accessible_ports = []

for port in range(from_scoket, to_scoket + 1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)
    result = s.connect_ex((ip, port))
    if result == 0:
        accessible_ports.append(port)
    s.close()

print("Accessible ports:", accessible_ports)
