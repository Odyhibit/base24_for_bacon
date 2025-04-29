# Base24 Python implementation compatible with the JavaScript version

base24_alphabet = "ABCDEFGHIKLMNOPQRSTUWXYZ"


def to_base24(message: str) -> str:
    """
    Encode a UTF-8 string into Base24 using a custom 24-symbol alphabet.
    The first two characters encode the byte-length.
    """
    # UTF-8 bytes
    b = message.encode('utf-8')
    length = len(b)

    # Build a big integer from the bytes
    big_int = int.from_bytes(b, 'big')

    # Convert big integer to base24 representation
    if big_int == 0:
        result = base24_alphabet[0]
    else:
        result = ""
        while big_int > 0:
            remainder = big_int % 24
            result = base24_alphabet[remainder] + result
            big_int //= 24

    # Prepend the length (2 base24 characters)
    length_val = length
    length_encoded = ""
    for _ in range(2):
        length_encoded = base24_alphabet[length_val % 24] + length_encoded
        length_val //= 24

    return length_encoded + result


def from_base24(encoded: str) -> str:
    """
    Decode a Base24 string (with 2-char length prefix) back to UTF-8.
    """
    if not encoded or len(encoded) < 2:
        return ""

    # Decode the length prefix
    length = 0
    for c in encoded[:2]:
        idx = base24_alphabet.find(c)
        if idx == -1:
            raise ValueError(f"Invalid Base24 character in length: {c}")
        length = length * 24 + idx

    # Decode the data portion into a big integer
    big_int = 0
    for c in encoded[2:]:
        idx = base24_alphabet.find(c)
        if idx == -1:
            raise ValueError(f"Invalid Base24 character in data: {c}")
        big_int = big_int * 24 + idx

    # Convert big integer back into bytes of the right length
    b = big_int.to_bytes(length, 'big')

    # Decode UTF-8
    return b.decode('utf-8')


# Quick test to verify round-trip (including emoji):
for s in ["hello", "ABC123", "😀😀😀"]:
    enc = to_base24(s)
    dec = from_base24(enc)
    print(f"{s!r} → {enc} → {dec!r}")

print(f"JavaScript encoded: 'This is a smiley face -> 😊'\n {from_base24('BFCFHGMRKFPHUSPYYXUXHWQUNCHIXZUMLTGRRCYZNLILUESOQUSDC')}")