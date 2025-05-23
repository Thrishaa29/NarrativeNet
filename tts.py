import streamlit as st
import requests

import requests
import tempfile
import os
import streamlit as st

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
            st.error(f"TTS failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"TTS exception: {e}")
        return None


