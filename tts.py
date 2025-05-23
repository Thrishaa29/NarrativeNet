import streamlit as st
import requests
import tempfile

def speak(text):
    try:
        API_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
        headers = {"Authorization": f"Bearer {st.secrets['HF_API_KEY']}"}

        st.info("Sending request to TTS model...")
        response = requests.post(API_URL, headers=headers, json={"inputs": text})

        st.write(f"Status Code: {response.status_code}")
        st.write(f"Content-Type: {response.headers.get('content-type')}")
        st.write("Response Preview:", response.content[:500])  # Log preview of content

        if response.status_code == 503:
            st.warning("TTS model is warming up. Please try again shortly.")
            return None

        if response.status_code == 200 and response.headers.get("content-type", "").startswith("audio/"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                f.write(response.content)
                return f.name
        else:
            st.error(f"TTS API returned unexpected content:\n{response.status_code} - {response.text}")
            return None

    except Exception as e:
        st.exception(f"Exception in speak(): {e}")
        return None

def main():
    st.title("Text-to-Speech (TTS) Demo")
    text = st.text_area("Enter text to speak")

    if st.button("Generate Audio"):
        if not text.strip():
            st.warning("Please enter some text.")
        else:
            audio_path = speak(text)
            if audio_path:
                with open(audio_path, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format="audio/wav")
            else:
                st.error("Could not generate audio. See above for error details.")

if __name__ == "__main__":
    main()

