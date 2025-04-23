import streamlit as st

# Page selector
page = st.sidebar.selectbox("Select Page", ["Encoder & Decoder", "How It Works"])

# ----------------- PAGE 1: ENCODER / DECODER -----------------
if page == "Encoder & Decoder":
    st.title("Message Encoder & Decoder")

    method = st.selectbox("Select Method", ["Substitution", "Replacement"])
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

    # Always show result box
    st.text_area("Result", output, height=150)

# ----------------- PAGE 2: HOW IT WORKS -----------------
elif page == "How It Works":
    st.title("How the Encoder & Decoder Work")

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

    st.success("Tip: Use the sidebar to return to the encoder/decoder.")
