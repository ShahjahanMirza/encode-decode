import streamlit as st

# Page selector
page = st.sidebar.selectbox("Select Page", ["🔐 Encoder & Decoder", "📘 How It Works"])

# ----------------- PAGE 1: ENCODER / DECODER -----------------
if page == "🔐 Encoder & Decoder":
    st.title("Message Encoder & Decoder")

    method = st.selectbox("Select Method", ["Substitution", "Replacement", "Vigenere"])
    mode = st.radio("Choose Mode", ["Encode", "Decode"])
    message = st.text_area("Enter your message")

    # Substitution logic
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

    # Replacement logic
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

    # Vigenere logic
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

    # Default result
    output = ""

    # Main logic
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

    st.markdown("**Vigenère Table (Simplified)**")

    import pandas as pd
    import string

    table_data = []
    letters = list(string.ascii_uppercase)
    for i in range(26):
        row = [letters[i]] + [letters[(j + i) % 26] for j in range(26)]
        table_data.append(row)

    df = pd.DataFrame(table_data, columns=["Key\\Char"] + letters)
    st.dataframe(df)

    st.success("Tip: Use the sidebar to return to the encoder/decoder.")
