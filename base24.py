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


base24_alphabet = "ABCDEFGHIKLMNOPQRSTUWXYZ"


def to_base24(message):
    """
    Encode a string to Base24, preserving Unicode characters including emojis.

    Args:
        message (str): The message to encode

    Returns:
        str: The Base24 encoded string
    """
    # Convert message to UTF-8 bytes
    bytes_data = message.encode('utf-8')

    # Convert bytes to a single big integer
    big_int = int.from_bytes(bytes_data, byteorder='big')

    # Store the length of bytes for decoding
    length = len(bytes_data)

    # Convert to base24
    result = ""
    if big_int == 0:
        return base24_alphabet[0]

    while big_int > 0:
        remainder = big_int % 24
        result = base24_alphabet[remainder] + result
        big_int = big_int // 24

    # Store the length at the beginning (use 2 base24 chars for length)
    length_encoded = ""
    length_value = length
    for _ in range(2):
        remainder = length_value % 24
        length_encoded = base24_alphabet[remainder] + length_encoded
        length_value = length_value // 24

    return length_encoded + result


def from_base24(encoded):
    """
    Decode a Base24 encoded string back to the original string.

    Args:
        encoded (str): The Base24 encoded string

    Returns:
        str: The decoded string with Unicode characters preserved
    """
    if not encoded or len(encoded) < 2:
        return ""

    # Extract length info from the first 2 characters
    length_chars = encoded[:2]
    length = 0
    for char in length_chars:
        if char not in base24_alphabet:
            raise ValueError(f"Invalid Base24 character: {char}")
        char_value = base24_alphabet.index(char)
        length = length * 24 + char_value

    # Extract the actual encoded data
    data_chars = encoded[2:]

    # Convert base24 to a big integer
    big_int = 0
    for char in data_chars:
        if char not in base24_alphabet:
            raise ValueError(f"Invalid Base24 character: {char}")
        char_value = base24_alphabet.index(char)
        big_int = big_int * 24 + char_value

    # Convert big integer to bytes
    try:
        bytes_data = big_int.to_bytes(length, byteorder='big')
    except OverflowError:
        # Handle case where the decoded length might be incorrect
        return "Error: Could not decode the data correctly"

    # Decode bytes to string
    try:
        return bytes_data.decode('utf-8')
    except UnicodeDecodeError:
        return "Error: Invalid UTF-8 sequence"


# Example usage
def main():
    # Test with different types of text including emojis
    test_messages = [
        "Hello, World!",
        "Testing 123",
        "Emoji test: 😀 🌍 🚀",
        "Mixed text and emoji: Hello 👋 World 🌎!"
    ]

    for message in test_messages:
        print(f"\nOriginal: {message}")
        encoded = to_base24(message)
        print(f"Encoded: {encoded}")
        decoded = from_base24(encoded)
        print(f"Decoded: {decoded}")
        print(f"Match: {message == decoded}")


if __name__ == "__main__":
    main()
