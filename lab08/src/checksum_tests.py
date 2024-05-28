from shared import calculate_checksum, verify_checksum


data = bytes([0x10, 0x02, 0x31, 0x14])
assert verify_checksum(data, calculate_checksum(data))

data = bytes([0x10, 0x02, 0x31, 0x14])
assert not verify_checksum(data, calculate_checksum(data) + 1)

data = bytes([0x12, 0x34, 0x56, 0x78])
corrupted_data = bytes([0x13, 0x34, 0x56, 0x78])
assert verify_checksum(corrupted_data, calculate_checksum(data))

print("All good!")
