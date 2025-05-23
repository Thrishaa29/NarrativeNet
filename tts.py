import json
import requests
import tempfile
import streamlit as st

# Hugging Face TTS model URL
API_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"

def speak(text):
    try:
        headers = {
            "Authorization": f"Bearer {st.secrets['HF_API_KEY']}",
            "X-Wait-For-Model": "true"
        }

        # Create payload and send request
        payload = {"inputs": text}
        data = json.dumps(payload)
        response = requests.post(API_URL, headers=headers, data=data)

        # Check for success
        content_type = response.headers.get("content-type", "")
        if response.status_code == 200 and content_type.startswith("audio/"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                f.write(response.content)
                return f.name
        else:
            # Try to extract error message if it's JSON
            try:
                error_message = response.json().get("error", response.text)
            except:
                error_message = response.text
            st.error(f"TTS API Error: {response.status_code} - {error_message}")
            return None
    except Exception as e:
        st.exception(f"TTS Exception: {e}")
        return None


