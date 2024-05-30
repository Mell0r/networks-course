import json
import socket
from threading import Lock, Thread
from collections import defaultdict
from typing import Dict, List

type RoutingTable = Dict[str, int]

GLOBAL_IP = "127.0.0.1"


def print_routing_table(
    source_ip: str, routing_table: RoutingTable, next_hops: Dict[str, str]
):
    def print_router_data(source_ip, destination_ip, next_hop, cost):
        print(f"{source_ip:<15}{destination_ip:<20}{next_hop:<17}{cost:>8}")

    print_router_data("[Source IP]", "[Destination IP]", "[Next Hop]", "[Metric]")
    for destination, cost in routing_table.items():
        print_router_data(source_ip, destination, next_hops.get(destination, "*"), cost)
    print()


# def print_routing_tables(routing_tables : List[RoutingTable], next_hops):
#     for router_ip, routing_table in routing_tables.items():
#         print_routing_table(router_ip, routing_table, next_hops)


def get_router_port(ip: str, routers: List[str], is_status_port=False):
    for i in range(len(routers)):
        if routers[i] == ip:
            return 14000 + i + (len(routers) if is_status_port else 0)


def send_routing_table(
    socket: socket.socket,
    neighbour_ip: str,
    routing_table: RoutingTable,
    routers: list[str],
):
    socket.sendto(
        json.dumps(routing_table).encode(),
        (GLOBAL_IP, get_router_port(neighbour_ip, routers)),
    )


def receive_routing_table(socket: socket.socket) -> RoutingTable:
    return json.loads(socket.recv(1024).decode())


def send_table_updated_status(
    socket: socket.socket,
    neighbour_ip: str,
    table_updated: bool,
    routers: list[str],
):
    socket.sendto(
        table_updated.to_bytes(),
        (GLOBAL_IP, get_router_port(neighbour_ip, routers, True)),
    )


def receive_table_updated_status(socket: socket.socket) -> bool:
    data, _ = socket.recvfrom(1024)
    return bool.from_bytes(data)


logger_lock = Lock()


def run_router(routers: List[str], router_ip: str, neighbors: List[str]):
    routing_table: RoutingTable = defaultdict(lambda: int(1e9))
    next_hops: Dict[str, str] = {}
    routing_table[router_ip] = 0

    for neighbor in neighbors:
        routing_table[neighbor] = 1
        next_hops[neighbor] = neighbor

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as routing_table_socket:
        routing_table_socket.bind((GLOBAL_IP, get_router_port(router_ip, routers)))
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as status_socket:
            status_socket.bind((GLOBAL_IP, get_router_port(router_ip, routers, True)))
            step = 0
            table_updated = True
            while table_updated:
                step += 1
                table_updated = False

                for neighbor in neighbors:
                    send_routing_table(
                        routing_table_socket, neighbor, routing_table, routers
                    )

                for neighbor in neighbors:
                    updated_table = receive_routing_table(routing_table_socket)

                    for destination_ip, cost in updated_table.items():
                        new_cost = cost + 1
                        if new_cost < routing_table[destination_ip]:
                            routing_table[destination_ip] = new_cost
                            next_hops[destination_ip] = neighbor
                            table_updated = True

                logger_lock.acquire()
                print(f"Simulation step {step} of router {router_ip}")
                print_routing_table(router_ip, routing_table, next_hops)
                logger_lock.release()

                for host in routers:
                    send_table_updated_status(
                        status_socket, host, table_updated, routers
                    )

                for host in routers:
                    neighbor_has_changes = receive_table_updated_status(status_socket)
                    table_updated |= neighbor_has_changes

    logger_lock.acquire()
    print(f"Final state of router {router_ip} table:")
    print_routing_table(router_ip, routing_table, next_hops)
    logger_lock.release()


with open("config.json") as f:
    config: Dict[str, List[str]] = json.load(f)
routers = list(config.keys())
threads = [
    Thread(target=run_router, args=(routers, router, neighbours))
    for router, neighbours in config.items()
]

for t in threads:
    t.start()

for t in threads:
    t.join()
