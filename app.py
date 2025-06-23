
import streamlit as st
from tts import speak
from story_generator import generate_novel_cached, split_into_chapters
import os
from dotenv import load_dotenv
import streamlit.components.v1 as components

load_dotenv()

# ---------- Streamlit Setup ----------
st.set_page_config(page_title="NarrativeNet Novel Generator", layout="wide")

# Load custom CSS if available
if os.path.exists("themes.css"):
    st.markdown("<style>" + open("themes.css").read() + "</style>", unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    body { background-color: #1e1e2f; color: #ffffff; }
    h1, h2, h3 { color: #ffcc70; }
    .stButton>button { background-color: #ff7e5f; color: white; border-radius: 12px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# ---------- App Title ----------
st.title("📚 NarrativeNet: AI-Driven Novel Generation")

st.markdown("""
Welcome to the Novel Generator! Create complete novels in your favorite genre.
Choose a genre below and optionally add your own beginning to the story.
""")

# ---------- Session State Setup ----------
if 'generating' not in st.session_state:
    st.session_state.generating = False
if 'novel' not in st.session_state:
    st.session_state.novel = None
if 'current_chapter' not in st.session_state:
    st.session_state.current_chapter = 0

# ---------- User Input ----------
genre_options = {
    "Fantasy": "Fantasy (magic, creatures, quests)",
    "Sci-Fi": "Sci-Fi (technology, space, aliens)",
    "Mystery": "Mystery (detectives, cases, clues)",
    "Adventure": "Adventure (exploration, treasure, journeys)",
    "Horror": "Horror (suspense, fear, supernatural)"
}
genre = st.selectbox("Select Novel Genre", list(genre_options.keys()), format_func=lambda x: genre_options[x])

user_prompt = st.text_input("Your Novel Beginning (optional)", placeholder="Enter a few words to start your novel")

chapter_count = st.slider("Number of Chapters", min_value=2, max_value=5, value=3)

enable_tts = st.toggle("🔊 Enable Voice Narration", value=False)

# ---------- Generate Novel Callback ----------
def generate_button_callback():
    st.session_state.generating = True
    st.session_state.novel = None
    st.session_state.current_chapter = 0

generate_btn = st.button("✨ Generate Novel", on_click=generate_button_callback)

# ---------- Novel Display ----------
def display_novel(novel_text, current_idx, enable_tts=False):
    if novel_text.startswith("Error"):
        st.error(novel_text)
        return

    title_line = novel_text.split('\n')[0] if '\n' in novel_text else "Generated Novel"
    title = title_line.replace('# ', '') if title_line.startswith('# ') else title_line
    st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)

    chapters = split_into_chapters(novel_text)

    with st.expander("📑 Table of Contents", expanded=True):
        for i, chapter in enumerate(chapters):
            chapter_title = chapter.split('\n')[0] if '\n' in chapter else f"Chapter {i+1}"
            if st.button(chapter_title, key=f"toc_{i}"):
                st.session_state.current_chapter = i
                st.rerun()

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if current_idx > 0 and st.button("◀️ Previous"):
            st.session_state.current_chapter -= 1
            st.rerun()
    with col3:
        if current_idx < len(chapters) - 1 and st.button("Next ▶️"):
            st.session_state.current_chapter += 1
            st.rerun()

    st.markdown("---")
    current_chapter = chapters[current_idx]
    st.markdown(current_chapter, unsafe_allow_html=True)

    if enable_tts:
        if st.secrets.get("IS_DEPLOYED", False):
            components.html(f"""
                <script>
                    var msg = new SpeechSynthesisUtterance("{current_chapter.replace('"', '')}");
                    window.speechSynthesis.speak(msg);
                </script>
            """, height=0)
        else:
            speak(current_chapter)

# ---------- Generate Logic ----------
if st.session_state.generating:
    progress_placeholder = st.empty()
    with progress_placeholder.container():
        st.write("🔮 Generating your novel... Please wait.")
        st.progress(50)

    try:
        novel = generate_novel_cached(genre, user_prompt, num_chapters=chapter_count)
        st.session_state.novel = novel
        st.session_state.generating = False
        progress_placeholder.empty()
        st.experimental_rerun()
    except Exception as e:
        st.session_state.generating = False
        st.error(f"⚠️ Generation failed: {str(e)}")

# ---------- Display If Generated ----------
if not st.session_state.generating and st.session_state.novel:
    display_novel(
        st.session_state.novel,
        st.session_state.current_chapter,
        enable_tts
    )

    st.download_button(
        label="📥 Download Novel as Text",
        data=st.session_state.novel,
        file_name=f"{genre.lower()}_novel.txt",
        mime="text/plain"
    )
