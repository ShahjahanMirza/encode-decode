import streamlit as st
import pandas as pd
import string

# Page selector
page = st.sidebar.selectbox("Select Page", ["🔐 Encoder & Decoder", "📘 How It Works"])

# ----------------- PAGE 1: ENCODER / DECODER -----------------
if page == "🔐 Encoder & Decoder":
    st.title("Message Encoder & Decoder")

    method = st.selectbox("Select Method", ["Substitution", "Replacement", "Vigenere", "Rail Fence", "Columnar"])
    mode = st.radio("Choose Mode", ["Encode", "Decode"])
    message = st.text_area("Enter your message")

    # Substitution Cipher
    def substitution(text, shift, encode=True):
        result = ""
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                shift_amount = shift if encode else -shift
                new_char = chr((ord(char) - base + shift_amount) % 26 + base)
                result += new_char
            else:
                result += char
        return result

    # Replacement Cipher
    replacement_dict = {
        'A': "x1z", 'B': "p9q", 'C': "m2n", 'D': "t7u", 'E': "l0k",
        'F': "b3v", 'G': "g4s", 'H': "y6w", 'I': "r5e", 'J': "a8j",
        'K': "z2x", 'L': "c7d", 'M': "q3f", 'N': "u1i", 'O': "h6o",
        'P': "v5b", 'Q': "n4m", 'R': "s9g", 'S': "e3t", 'T': "j2l",
        'U': "k1p", 'V': "d6h", 'W': "o7y", 'X': "i0u", 'Y': "f8a",
        'Z': "w5c"
    }
    reverse_replacement_dict = {v: k for k, v in replacement_dict.items()}

    def replacement_encode(text):
        result = ""
        for char in text.upper():
            result += replacement_dict.get(char, char)
        return result

    def replacement_decode(text):
        result = ""
        i = 0
        while i < len(text):
            chunk = text[i:i+3]
            if chunk in reverse_replacement_dict:
                result += reverse_replacement_dict[chunk]
                i += 3
            else:
                result += text[i]
                i += 1
        return result

    # Vigenère Cipher
    def vigenere(text, keyword, encode=True):
        result = ""
        keyword = keyword.lower()
        key_index = 0
        for char in text:
            if char.isalpha():
                shift = ord(keyword[key_index % len(keyword)]) - ord('a')
                if not encode:
                    shift = -shift
                base = ord('A') if char.isupper() else ord('a')
                new_char = chr((ord(char) - base + shift) % 26 + base)
                result += new_char
                key_index += 1
            else:
                result += char
        return result

    # Rail Fence Cipher
    def rail_fence_encode(text, rails):
        fence = [[] for _ in range(rails)]
        rail = 0
        direction = 1
        for char in text:
            fence[rail].append(char)
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction *= -1
        return ''.join([''.join(row) for row in fence])

    def rail_fence_decode(cipher, rails):
        rail_len = [0] * rails
        rail = 0
        direction = 1
        for _ in cipher:
            rail_len[rail] += 1
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction *= -1
        indexes = []
        i = 0
        for r in rail_len:
            indexes.append(cipher[i:i+r])
            i += r
        result = ""
        rail = 0
        direction = 1
        rail_pos = [0] * rails
        for _ in cipher:
            result += indexes[rail][rail_pos[rail]]
            rail_pos[rail] += 1
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction *= -1
        return result

    # Columnar Cipher
    def columnar_encode(text, keyword):
        text = text.replace(" ", "")
        k_len = len(keyword)
        sorted_key = sorted([(char, i) for i, char in enumerate(keyword)])
        columns = ['' for _ in range(k_len)]
        for i, char in enumerate(text):
            col = i % k_len
            columns[col] += char
        return ''.join(columns[i[1]] for i in sorted_key)

    def columnar_decode(cipher, keyword):
        k_len = len(keyword)
        n_rows = len(cipher) // k_len + (len(cipher) % k_len > 0)
        sorted_key = sorted([(char, i) for i, char in enumerate(keyword)])
        col_lens = [n_rows] * k_len
        total_cells = k_len * n_rows
        extra = total_cells - len(cipher)
        for i in range(extra):
            col_lens[sorted_key[-(i+1)][1]] -= 1
        cols = {}
        i = 0
        for char, original_pos in sorted_key:
            cols[original_pos] = cipher[i:i+col_lens[original_pos]]
            i += col_lens[original_pos]
        result = ""
        for row in range(n_rows):
            for col in range(k_len):
                if row < len(cols[col]):
                    result += cols[col][row]
        return result

    # Main logic
    output = ""

    if method == "Substitution":
        shift = st.slider("Select Shift Value", 1, 25, 2)
        if message:
            output = substitution(message, shift, encode=(mode == "Encode"))

    elif method == "Replacement":
        if message:
            output = replacement_encode(message) if mode == "Encode" else replacement_decode(message)

    elif method == "Vigenere":
        keyword = st.text_input("Enter Keyword (letters only)")
        if message and keyword.isalpha():
            output = vigenere(message, keyword, encode=(mode == "Encode"))
        elif keyword and not keyword.isalpha():
            st.error("Keyword must only contain letters.")

    elif method == "Rail Fence":
        rails = st.slider("Select Number of Rails", 2, 10, 3)
        if message:
            if mode == "Encode":
                # Encode and show zigzag table
                output = rail_fence_encode(message, rails)

                # Build zigzag matrix
                fence = [[" " for _ in range(len(message))] for _ in range(rails)]
                rail = 0
                direction = 1
                for i, char in enumerate(message):
                    fence[rail][i] = char
                    rail += direction
                    if rail == 0 or rail == rails - 1:
                        direction *= -1

                st.markdown("### Zigzag Pattern")
                df = pd.DataFrame(fence)
                st.dataframe(df.style.set_properties(**{'text-align': 'center'}))

            else:
                output = rail_fence_decode(message, rails)


    elif method == "Columnar":
        keyword = st.text_input("Enter Keyword (letters only)")
        if message and keyword.isalpha():
            if mode == "Encode":
                output = columnar_encode(message, keyword)

                # Create table
                keyword_upper = keyword.upper()
                keyword_order = sorted([(char, idx) for idx, char in enumerate(keyword_upper)])
                sorted_indices = [idx for char, idx in keyword_order]

                # Pad message
                cols = len(keyword)
                rows = (len(message) + cols - 1) // cols
                padded = message.ljust(rows * cols, '_')

                # Fill matrix row-wise
                matrix = []
                for r in range(rows):
                    matrix.append(list(padded[r*cols:(r+1)*cols]))

                # Build dataframe for visualization
                df = pd.DataFrame(matrix, columns=list(keyword_upper))
                st.markdown("### Columnar Grid Before Rearranging")
                st.dataframe(df.style.set_properties(**{'text-align': 'center'}))

                # Show reordered columns
                reordered_df = df.iloc[:, sorted_indices]
                reordered_df.columns = [keyword_upper[i] for i in sorted_indices]
                st.markdown("### Columns Rearranged by Alphabetical Order of Keyword")
                st.dataframe(reordered_df.style.set_properties(**{'text-align': 'center'}))

            else:
                output = columnar_decode(message, keyword)

        elif keyword and not keyword.isalpha():
            st.error("Keyword must only contain letters.")


    st.text_area("Result", output, height=150)

# ----------------- PAGE 2: HOW IT WORKS -----------------
elif page == "📘 How It Works":
    st.title("📘 How the Encoder & Decoder Work")

    st.header("1. Substitution Method")
    st.markdown("""
    This method shifts letters in your message by a fixed amount.

    - Example with shift = 2:
      - A → C
      - B → D
      - Z → B
    - It wraps around the alphabet and keeps punctuation unchanged.
    - Decoding uses the reverse shift.

    **Example:**  
    `HELLO` → (shift=2) → `JGNNQ`
    """)

    st.header("2. Replacement Method")
    st.markdown("""
    This method uses a fixed dictionary to replace each uppercase letter with a 3-character code.

    - A → x1z  
    - B → p9q  
    - etc.

    It's best for hiding patterns, but decoding requires exact chunking every 3 letters.

    **Example:**  
    `ABC` → `x1zp9qm2n`  
    Then decoded back to `ABC`
    """)

    st.header("3. Vigenère Cipher")
    st.markdown("""
    This method uses a keyword to determine the shift for each letter in the message.

    - A letter in the keyword determines how much to shift a letter in the message.
    - It's a form of polyalphabetic substitution.

    **Example:**  
    Keyword = `KEY`, Message = `HELLO`  
    Convert keyword to shifts:  
    - K (10), E (4), Y (24), K (10), E (4)  
    - H+10 → R, E+4 → I, L+24 → J, L+10 → V, O+4 → S  
    - `HELLO` → `RIJVS`
    """)

    st.header("4. Rail Fence Cipher")
    st.markdown("""
    The Rail Fence Cipher is a transposition cipher that writes your message in a zigzag pattern on a set number of "rails".

    - Encoding writes the message in zigzag and reads line by line.
    - Decoding reconstructs the zigzag pattern.

    **Example:**  
    Message: `HELLOWORLD`, Rails: 3  
    Zigzag:
    ```
    H   L   W   L
     E L O O R D
      L   O   D
    ```
    Encoded: `HLOELORDLW`
    """)

    st.header("5. Columnar Transposition")
    st.markdown("""
    This method arranges text in a grid using the keyword length, then reads columns in the order of sorted keyword letters.

    - Encoding reorders columns by the alphabetical order of the keyword.
    - Decoding builds the grid and reads row by row.

    **Example:**  
    Message: `WEAREDISCOVERED`, Keyword: `ZEBRAS`  
    Keyword order: A (1), B (2), E (3), R (4), S (5), Z (6)  
    Rearranged columns are joined to get the encoded message.
    """)

    st.markdown("**Vigenère Table (Simplified)**")
    table_data = []
    letters = list(string.ascii_uppercase)
    for i in range(26):
        row = [letters[i]] + [letters[(j + i) % 26] for j in range(26)]
        table_data.append(row)
    df = pd.DataFrame(table_data, columns=["Key\\Char"] + letters)
    st.dataframe(df)

    st.success("Tip: Use the sidebar to return to the encoder/decoder.")
