# 📚 NarrativeNet

**NarrativeNet** is an AI-powered novel generation and narration app built with Streamlit. Users can generate stories by selecting a genre and providing a prompt, then read or listen to the story chapter by chapter.
Access the deployed app here https://narattivenet.streamlit.app/
---

## 🚀 Features

- ✅ Generate full-length novels using AI
- ✅ Choose from popular genres like Fantasy, Sci-Fi, Mystery, Adventure, and Horror
- ✅ Navigate through chapters with a clean, interactive UI
- ✅ **(Local only)** Listen to generated chapters with real-time text-to-speech (TTS)

---

## 🔊 Text-to-Speech Support (TTS)

> ⚠️ **Important Notice:**  
> Text-to-speech (TTS) functionality is only available when running **NarrativeNet locally**.  
> Due to limitations of the Streamlit Cloud platform, audio playback from system-level TTS engines (like `pyttsx3`) is not supported in deployed environments.

### How it works locally:
- Uses the `pyttsx3` library for offline speech synthesis
- Audio is generated and played directly on your device
- Works on macOS, Windows, and Linux with Python 3.8+

---

## 🛠 Installation

### 1. Clone the repo

```bash 
git clone https://github.com/yourusername/narrativenet.git
cd narrativenet
```
2. Create a virtual environment

 ```bash 
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Run the app locally
```bash
streamlit run app.py
```
✅ At this point, both novel generation and audio narration will work.

📦 Deployment (Without Audio)
You can deploy NarrativeNet to Streamlit Cloud for online use, but:
1.Text-to-speech will not function
2.Users will still be able to generate and read novels

To deploy:
1.Push your code to GitHub
2.Connect the repo at https://streamlit.io/cloud
3.Set up secrets and dependencies

🧠 Future Improvements
Add cloud-compatible TTS (e.g., Hugging Face API)
Support downloadable audiobook files
Improve voice quality and options


