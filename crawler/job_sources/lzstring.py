"""위시켓 목록 필터에 쓰는 LZString.compressToBase64.

페이지 번호만 `page=N` 형태로 압축한다.
"""

from __future__ import annotations

_KEY = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="


def compress_to_base64(value: str) -> str:
    if value is None:
        return ""
    compressed = _compress(value, 6, lambda code: _KEY[code])
    pad = (4 - len(compressed) % 4) % 4
    return compressed + ("=" * pad)


def _compress(uncompressed: str, bits_per_char: int, get_char) -> str:
    dictionary: dict[str, int] = {}
    dictionary_to_create: dict[str, bool] = {}
    w = ""
    enlarge_in = 2
    dict_size = 3
    num_bits = 2
    data: list[str] = []
    data_val = 0
    data_position = 0

    def write_bit(bit: int) -> None:
        nonlocal data_val, data_position
        data_val = (data_val << 1) | bit
        if data_position == bits_per_char - 1:
            data_position = 0
            data.append(get_char(data_val))
            data_val = 0
        else:
            data_position += 1

    def write_repeated(bit: int, count: int) -> None:
        for _ in range(count):
            write_bit(bit)

    def write_value(value: int, count: int) -> None:
        for _ in range(count):
            write_bit(value & 1)
            value >>= 1

    for c in uncompressed:
        if c not in dictionary:
            dictionary[c] = dict_size
            dict_size += 1
            dictionary_to_create[c] = True
        wc = w + c
        if wc in dictionary:
            w = wc
            continue
        if w in dictionary_to_create:
            if ord(w[0]) < 256:
                write_repeated(0, num_bits)
                write_value(ord(w[0]), 8)
            else:
                write_repeated(1, num_bits)
                write_value(ord(w[0]), 16)
            enlarge_in -= 1
            if enlarge_in == 0:
                enlarge_in = 2**num_bits
                num_bits += 1
            del dictionary_to_create[w]
        else:
            write_value(dictionary[w], num_bits)
        enlarge_in -= 1
        if enlarge_in == 0:
            enlarge_in = 2**num_bits
            num_bits += 1
        dictionary[wc] = dict_size
        dict_size += 1
        w = c

    if w != "":
        if w in dictionary_to_create:
            if ord(w[0]) < 256:
                write_repeated(0, num_bits)
                write_value(ord(w[0]), 8)
            else:
                write_repeated(1, num_bits)
                write_value(ord(w[0]), 16)
            enlarge_in -= 1
            if enlarge_in == 0:
                enlarge_in = 2**num_bits
                num_bits += 1
            del dictionary_to_create[w]
        else:
            write_value(dictionary[w], num_bits)
        enlarge_in -= 1
        if enlarge_in == 0:
            enlarge_in = 2**num_bits
            num_bits += 1

    write_value(2, num_bits)
    while True:
        data_val <<= 1
        if data_position == bits_per_char - 1:
            data.append(get_char(data_val))
            break
        data_position += 1
    return "".join(data)
