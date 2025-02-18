import struct


class Base24:
    alphabet = "ABCDEFGHIKLMNOPQRSTVWXYZ"
    alphabet_length = 24
    encode_map = {}
    decode_map = {}

    for idx, char in enumerate(alphabet):
        encode_map[idx] = char
        decode_map[char] = idx
        decode_map[char.lower()] = idx  # Case-insensitive mapping


    @staticmethod
    def encode24(data: bytes) -> str:
        if len(data) % 4 != 0:
            raise Exception("Encode 24 data length must be a multiple of 4 bytes (32 bits)")

        result = []

        for i in range(len(data) // 4):
            j = i * 4
            mask = 0xFF
            b3 = data[j] & mask
            b2 = data[j + 1] & mask
            b1 = data[j + 2] & mask
            b0 = data[j + 3] & mask

            value = 0xFFFFFFFF & ((b3 << 24) | (b2 << 16) | (b1 << 8) | b0)
            print(value)
            sub_result = []
            for _ in range(7):
                idx = value % Base24.alphabet_length
                value //= Base24.alphabet_length
                sub_result.insert(0, Base24.encode_map[idx])

            result.append("".join(sub_result))

        return "".join(result)

    @staticmethod
    def decode24(data: str) -> bytes:
        if len(data) % 7 != 0:
            raise Exception("Decode 24 data length must be a multiple of 7 characters")

        bytes_out = bytearray()

        for i in range(len(data) // 7):
            j = i * 7
            sub_data = data[j:j + 7]
            value = 0

            for char in sub_data:
                if char not in Base24.decode_map:
                    raise Exception(f"Unsupported character in input: {char}")
                value = Base24.alphabet_length * value + Base24.decode_map[char]

            mask = 0xFF
            b0 = (value >> 24) & mask
            b1 = (value >> 16) & mask
            b2 = (value >> 8) & mask
            b3 = value & mask

            bytes_out.extend([b0, b1, b2, b3])

        return bytes(bytes_out)


if __name__ == "__main__":


    def get_digits(p: int, number_base: int) -> [int]:
        """Returns a list with the least significant digit first. In the number_base chosen."""
        p_list = []
        while p > 0:
            p_digit = p % number_base
            p_list.append(p_digit)
            p //= number_base
        return p_list


    def to_base(p: int, number_base: int) -> str:
        """Returns a string version of a number in a specific base. Used for displaying number"""
        symbols = "ABCDEFGHIKLMNOPQRSTVWXYZ"
        p_list = get_digits(p, number_base)[::-1]
        return "".join(symbols[i] for i in p_list)


    def bytes_to_int32_big_endian(data):
        """Convert 4 bytes from a bytearray into a signed int32 (big-endian).
            returns: List of integers
        """
        return [struct.unpack_from('>i', data, i)[0] for i in range(0, len(data), 4)]  # '>i' means big-endian int32


    def get_digits(p: int, number_base: int) -> [int]:
        """Returns a list with the least significant digit first. In the number_base chosen."""
        p_list = []
        while p > 0:
            p_digit = p % number_base
            p_list.append(p_digit)
            p //= number_base
        return p_list


    def to_base(p: int, number_base: int) -> str:
        """Returns a string version of a number in a specific base. Used for displaying number"""
        symbols = "ABCDEFGHIKLMNOPQRSTVWXYZ"  # add more symbols here (64)
        p_list = get_digits(p, number_base)[::-1]
        return "".join(symbols[i] for i in p_list)


    # Example usage
    text = "Hello".encode("utf-8")
    padding = 4 - len(text) % 4
    text += b"\x00" * padding
    encoded = Base24.encode24(text)
    print(f"Encoded: {encoded}")
    decoded = Base24.decode24(encoded)
    print(f"Decoded: {decoded.decode('utf-8')}")
    test_value = "AAAAABA"
    print(f"{test_value}: {Base24.decode24(test_value).hex()}")
    int_value = bytes_to_int32_big_endian(text)
    print(int_value)
    for i in range(len(int_value)):
        print(to_base(int_value[i], 24))

    print("Using bytes.to int")
    for i in range(0, len(text), 4):
        print(to_base(int.from_bytes(text[i:i+4], "big"), 24))

