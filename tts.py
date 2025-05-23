import streamlit as st
import requests
import tempfile

def speak(text):
    try:
        API_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
        headers = {"Authorization": f"Bearer {st.secrets['HF_API_KEY']}"}

        # Send request to the TTS model
        response = requests.post(API_URL, headers=headers, json={"inputs": text})

        # Check for cold start response
        if response.status_code == 503:
            st.warning("TTS model is warming up. Please try again in a few seconds.")
            return None

        # Check if response is valid audio
        if response.status_code == 200 and response.headers.get("content-type", "").startswith("audio/"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                f.write(response.content)
                return f.name
        else:
            st.error(f"TTS API returned non-audio content: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        st.error(f"TTS error: {e}")
        return None

# Example usage in a Streamlit app
def main():
    st.title("Text-to-Speech (TTS) with Hugging Face")
    text = st.text_area("Enter text to speak:")

    if st.button("Generate Speech"):
        if text.strip() == "":
            st.warning("Please enter some text.")
        else:
            audio_path = speak(text)
            if audio_path:
                with open(audio_path, 'rb') as audio_file:
                    st.audio(audio_file.read(), format='audio/wav')
            else:
                st.error("Could not generate audio.")

if __name__ == "__main__":
    main()
