 const base24_alphabet = "ABCDEFGHIKLMNOPQRSTUWXYZ";

        function getDigits(p, number_base) {
            let p_list = [];
            while (p > 0) {
                let p_digit = p % number_base;
                p_list.push(p_digit);
                p = Math.floor(p / number_base);
            }
            return p_list.reverse();
        }

        function toBase(p, number_base) {
            let p_list = getDigits(p, number_base);
            return p_list.map(i => base24_alphabet[i]).join("");
        }

        function toBase24(message) {
            let encoder = new TextEncoder();
            let messageBytes = encoder.encode(message);
            let base24_code = "";
            for (let i = 0; i < messageBytes.length; i += 4) {
                let chunk = messageBytes.slice(i, i + 4);
                let num = chunk.reduce((acc, byte) => (acc << 8) + byte, 0);
                base24_code += toBase(num, 24);
            }
            return base24_code;
        }

        function fromBase24(base24_code) {
            let decodedBytes = [];
            for (let i = 0; i < base24_code.length; i += 7) {
                let value = 0;
                for (let digit = 0; digit < 7 && i + digit < base24_code.length; digit++) {
                    value = 24 * value + base24_alphabet.indexOf(base24_code[i + digit]);
                }
                let byteArray = [];
                for (let j = 3; j >= 0; j--) {
                    byteArray[j] = value & 0xff;
                    value >>= 8;
                }
                decodedBytes.push(...byteArray);
            }
            return new TextDecoder().decode(new Uint8Array(decodedBytes)).replace(/\x00/g, '');
        }

        function encodeInput() {
            let inputText = document.getElementById("inputText").value;
            let encodedText = toBase24(inputText);
            document.getElementById("outputText").textContent = encodedText;
        }

        function decodeInput() {
            let inputText = document.getElementById("inputText").value;
            let decodedText = fromBase24(inputText);
            document.getElementById("outputText").textContent = decodedText;
        }
