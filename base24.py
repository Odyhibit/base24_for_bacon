base24_alphabet = "ABCDEFGHIKLMNOPQRSTVWXYZ"  # Bacon cipher alphabet


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


def to_base24(message: str) -> str:
    """Converts a string to a base24 code."""
    message = message.encode("utf-8")
    base24_code = ""
    for i in range(0, len(message), 4):
        base24_code += to_base(int.from_bytes(message[i:i + 4], "big"), 24)
    return base24_code


def from_base24(base24_code: str) -> str:
    """Converts a base24 code to a string."""
    decoded = ""
    for i in range(0, len(base24_code), 7):
        value = 0
        for digit in range(7):
            value = 24 * value + base24_alphabet.index(base24_code[i + digit])
        decoded += value.to_bytes(4, "big").decode("utf-8")
    return decoded


if __name__ == "__main__":
    # Example usage
    text = "Hello World!"

    print("Original text:", text)
    print("Base24 code:", to_base24(text))
    print("Decoded text:", from_base24(to_base24(text)))
