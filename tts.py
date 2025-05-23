import streamlit as st
import requests

st.title("TTS Diagnostic Test")

API_URL = "https://api-inference.huggingface.co/models/facebook/fastspeech2-en-ljspeech"
headers = {
    "Authorization": f"Bearer {st.secrets['HF_API_KEY']}",
    "X-Wait-For-Model": "true"
}

text = "Hello from Streamlit"

if st.button("Test TTS"):
    st.write("Sending request...")
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": text})

        st.write("Status Code:", response.status_code)
        st.write("Content-Type:", response.headers.get("content-type"))
        st.write("First 300 characters of response:", response.content[:300])

        if response.status_code == 200 and response.headers.get("content-type", "").startswith("audio/"):
            st.success("Audio was returned!")
            st.audio(response.content, format="audio/wav")
        else:
            st.error(f"Failed. Status: {response.status_code}, Content: {response.text}")

    except Exception as e:
        st.exception(f"Exception: {e}")
