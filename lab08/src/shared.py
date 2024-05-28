from random import random
import pickle
import socket as sck
from itertools import batched
from functools import reduce
from collections.abc import Buffer

type Address = tuple[str, int]


def send_with_chance(socket: sck.socket, data: Buffer, dist: Address):
    if random() > 0.3:
        socket.sendto(data, dist)


def recieve_file(socket: sck.socket, file_path: str) -> Address | None:
    last_accepted_package_number: int | None = None
    client = None
    while True:
        try:
            package, client = socket.recvfrom(1024)
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
                socket,
                pickle.dumps(
                    {"package_number": last_accepted_package_number, "data": "ACK"}
                ),
                client,
            )

        except Exception as e:
            error = f"Internal server error: '{e}'."
            if client is not None:
                socket.sendto(
                    pickle.dumps({"package_number": -1, "data": error}), client
                )
            print(error)
            break
    return client


def send_file(
    socket: sck.socket,
    file_path: str,
    timeout: float,
    address_to: Address,
):
    socket.settimeout(timeout)
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
                    socket,
                    pickle.dumps(
                        {
                            "package_number": package_number,
                            "data": chunk,
                        }
                    ),
                    address_to,
                )
                try:
                    data_encoded, _ = socket.recvfrom(1024)
                    data = pickle.loads(data_encoded)
                    if data["package_number"] == -1:
                        print(data["data"])
                        exit(-1)
                    if data["package_number"] == package_number:
                        package_number = 1 - package_number
                        ind += 1
                        print("ACK received. Moving to next chunk...")
                except sck.timeout:
                    print("Timeout. Resending chunk...")

        socket.sendto(b"eof", address_to)
        print("File successfully sent.")
    except Exception as e:
        error = f"Internal client error: '{e}'."
        socket.sendto(
            pickle.dumps({"package_number": -1, "data": error.encode()}),
            address_to,
        )
        print(error)
    socket.settimeout(None)


def calculate_checksum(data: bytes, k=16):
    return (
        ~reduce(
            lambda prev, new: (prev + int.from_bytes(new)) & 0xFFFF,
            batched(data, k),
            0,
        )
        & 0xFFFF
    )


def verify_checksum(data, checksum: int, k: int = 16):
    return (~calculate_checksum(data, k) & 0xFFFF) + checksum == 0xFFFF
