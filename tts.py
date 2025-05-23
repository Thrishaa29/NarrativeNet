import streamlit as st
import requests
import tempfile

def speak(text):
    try:
        API_URL = "https://api-inference.huggingface.co/models/facebook/fastspeech2-en-ljspeech"
        headers = {
            "Authorization": f"Bearer {st.secrets['HF_API_KEY']}",
            "X-Wait-For-Model": "true"
        }

        response = requests.post(API_URL, headers=headers, json={"inputs": text})

        if response.status_code == 200 and response.headers.get("content-type", "").startswith("audio/"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                f.write(response.content)
                return f.name
        else:
            st.error(f"TTS API error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"TTS error: {e}")
        return None

def main():
    st.title("Text-to-Speech (Cloud-Ready)")
    text = st.text_area("Enter text to speak")

    if st.button("Generate Speech"):
        if text.strip():
            audio_path = speak(text)
            if audio_path:
                with open(audio_path, "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/wav")
            else:
                st.error("Failed to generate audio.")
        else:
            st.warning("Please enter some text.")

if __name__ == "__main__":
    main()
