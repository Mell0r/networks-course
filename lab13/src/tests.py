from crc import crc_encode, crc_check
from itertools import batched
from random import random

data = b"Hey there!"
generator = "101011"
data_encoded = crc_encode(data, generator)
assert crc_check(
    data_encoded, generator
), f"Simple correct crc encode fail: \n data={data} \n data_encoded={data_encoded} \n on generator={generator}"

data = b"Hey there!"
generator = "1011"
data_encoded = crc_encode(data, generator)
corrupted_data = str(int.from_bytes(data_encoded) ^ 1000).encode()
assert not crc_check(
    corrupted_data, generator
), f"Simple incorrect crc encode fail: \n data={data} \n data_encoded={data_encoded} \n corrupted_data={corrupted_data} \n on generator={generator}"

print("Simple tests passed")

data = b"Looooooooooooooooooooooooooooooooooooooooooooooooong text"
generator = "100111"
for ind, package in enumerate(batched(data, 5)):
    package_encoded = crc_encode(bytes(data), generator)
    corrupted = random() < 0.3
    data_maybe_corrupted = (
        (int.from_bytes(package_encoded) ^ (1 << int(39 * random()))).to_bytes(
            len(package_encoded)
        )
        if corrupted
        else package_encoded
    )

    print(f"Package {ind}:")
    print(f"Data: {package}")
    print(f"Data encoded: {package_encoded}")

    assert (
        crc_check(data_maybe_corrupted, generator) != corrupted
    ), f"Long text fail on package {ind}: package={package} package_encoded={package_encoded} on generator={generator}"

print("Long random text passed")
