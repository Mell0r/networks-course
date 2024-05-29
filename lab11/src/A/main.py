import socket
import time
import sys

target = sys.argv[1]
each_router_ping_count = int(sys.argv[2])

target_ip = socket.gethostbyname(target)

for ttl in range(1, 31):
    ttl_exceeded = False
    rtt_times = []
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    icmp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    icmp_socket.settimeout(2)

    print("{:>2}  ".format(ttl), end="")

    for i in range(each_router_ping_count):
        send_time = time.time()
        package = b"\x08\x00\xf7\xff\x00\x00\x00\x00"
        icmp_socket.sendto(package, (target_ip, 0))
        router_ip = None
        router_name = None
        try:
            recv_packet, addr = icmp_socket.recvfrom(1024)
            router_ip = addr[0]
            rtt = time.time() - send_time
            print("{:>4} ms ".format(int(rtt * 100)), end="")
            try:
                router_name = socket.gethostbyaddr(addr[0])[0]
            except socket.herror:
                pass
        except socket.timeout:
            print("   *    ", end="")

    print(f" {router_ip} [{router_name}]")
    icmp_socket.close()
    if router_ip == target_ip:
        break
