const base24_alphabet = "ABCDEFGHIKLMNOPQRSTUWXYZ";

function toBase24(message) {
    // Use TextEncoder to convert the string to UTF-8 bytes
    let encoder = new TextEncoder();
    let bytes = encoder.encode(message);

    // Convert bytes to a single big integer
    let bigInt = 0n;
    for (let i = 0; i < bytes.length; i++) {
        bigInt = (bigInt << 8n) | BigInt(bytes[i]);
    }

    // Store the length of bytes for decoding
    let length = bytes.length;

    // Convert to base24
    let result = "";
    if (bigInt === 0n) {
        return base24_alphabet[0];
    }

    while (bigInt > 0n) {
        let remainder = Number(bigInt % 24n);
        result = base24_alphabet[remainder] + result;
        bigInt = bigInt / 24n;
    }

    // Store the length at the beginning (use 2 base24 chars for length)
    let lengthEncoded = "";
    let lengthValue = length;
    for (let i = 0; i < 2; i++) {
        let remainder = lengthValue % 24;
        lengthEncoded = base24_alphabet[remainder] + lengthEncoded;
        lengthValue = Math.floor(lengthValue / 24);
    }

    return lengthEncoded + result;
}

function fromBase24(encoded) {
    if (!encoded || encoded.length < 2) {
        return "";
    }

    // Extract length info from the first 2 characters
    let lengthChars = encoded.substring(0, 2);
    let length = 0;
    for (let i = 0; i < lengthChars.length; i++) {
        let charValue = base24_alphabet.indexOf(lengthChars[i]);
        if (charValue === -1) {
            console.error(`Invalid Base24 character: ${lengthChars[i]}`);
            return "";
        }
        length = length * 24 + charValue;
    }

    // Extract the actual encoded data
    let dataChars = encoded.substring(2);

    // Convert base24 to a big integer
    let bigInt = 0n;
    for (let i = 0; i < dataChars.length; i++) {
        let charValue = base24_alphabet.indexOf(dataChars[i]);
        if (charValue === -1) {
            console.error(`Invalid Base24 character: ${dataChars[i]}`);
            return "";
        }
        bigInt = bigInt * 24n + BigInt(charValue);
    }

    // Convert big integer to bytes
    let bytes = new Uint8Array(length);
    for (let i = length - 1; i >= 0; i--) {
        bytes[i] = Number(bigInt & 0xFFn);
        bigInt = bigInt >> 8n;
    }

    // Decode bytes to string
    return new TextDecoder().decode(bytes);
}

function encodeInput() {
    let inputText = document.getElementById("inputText").value;
    let encodedText = toBase24(inputText);
    document.getElementById("outputText").value = encodedText;
}

function decodeInput() {
    let inputText = document.getElementById("inputText").value;
    let decodedText = fromBase24(inputText);
    document.getElementById("outputText").value = decodedText;
}

// Debug function to see what's happening
function debugEncodeDecode(text) {
    console.log("Original:", text);
    let encoder = new TextEncoder();
    let bytes = encoder.encode(text);
    console.log("UTF-8 bytes:", Array.from(bytes));

    let encoded = toBase24(text);
    console.log("Base24 encoded:", encoded);

    let decoded = fromBase24(encoded);
    console.log("Decoded:", decoded);

    return { original: text, bytes, encoded, decoded };
}