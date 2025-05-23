import streamlit as st
import requests
import tempfile

def speak(text):
    try:
        API_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
        headers = {"Authorization": f"Bearer {st.secrets['HF_API_KEY']}"}

        response = requests.post(API_URL, headers=headers, json={"inputs": text})

        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                f.write(response.content)
                return f.name
        else:
            st.error(f"TTS API error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"TTS error: {e}")
        return None
