from math import ceil, log


def get_reminder(n: int, m: int) -> int:
    n_length = ceil(log(n + 1, 2))
    m_length = ceil(log(m + 1, 2))
    not_xored_tail = n_length - m_length

    while n >= m or not_xored_tail >= 0:
        rem = (n >> not_xored_tail) ^ m
        n = (rem << not_xored_tail) | (n & ((1 << not_xored_tail) - 1))
        not_xored_tail = ceil(log(n + 1, 2)) - m_length
    return n


def crc_encode(data: bytes, generator: str) -> bytes:
    gen_length = len(generator)
    data_int = int.from_bytes(data)

    dividend = data_int << (gen_length - 1)
    divisor = int(generator, 2)
    return (data_int << (gen_length - 1) | get_reminder(dividend, divisor)).to_bytes(
        len(data) + ceil(gen_length / 8)
    )


def crc_check(data_encoded: bytes, generator: str) -> bool:
    return get_reminder(int.from_bytes(data_encoded), int(generator, 2)) == 0
