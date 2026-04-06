import streamlit as st
import cv2
from deepface import DeepFace
import yt_dlp
import random

# ---------------- UI ----------------
st.set_page_config(page_title="AI Music Recommender", layout="wide")

st.markdown("""
<style>
body {
    background-color: #121212;
}
.title {
    text-align:center;
    font-size:45px;
    color:#1DB954;
    font-weight:bold;
}
.song-card {
    background-color:#181818;
    padding:15px;
    border-radius:10px;
    margin-bottom:15px;
    transition: 0.3s;
}
.song-card:hover {
    transform: scale(1.03);
    background-color:#282828;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎧 AI Mood Music Player</div>', unsafe_allow_html=True)

# ---------------- CAMERA ----------------
st.subheader("📷 Live Emotion Detection")

run = st.checkbox("Start Camera")

FRAME_WINDOW = st.image([])
camera = cv2.VideoCapture(0)

emotion = "neutral"

if run:
    ret, frame = camera.read()

    if ret:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(rgb)

        try:
            result = DeepFace.analyze(rgb, actions=['emotion'], enforce_detection=False)
            emotion = result[0]['dominant_emotion']
        except:
            emotion = "neutral"

        st.success(f"Detected Emotion: {emotion}")

else:
    camera.release()

# ---------------- LANGUAGE ----------------
st.subheader("🌐 Select Language")

language = st.selectbox(
    "Choose Language",
    ["Hindi", "English", "Marathi", "Punjabi"]
)

# ---------------- YOUTUBE SEARCH ----------------
def get_youtube_songs(query, max_results=10):
    ydl_opts = {
        "quiet": True,
        "extract_flat": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        results = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)

    songs = []

    for entry in results['entries']:
        title = entry.get('title')
        video_id = entry.get('id')

        if title and video_id:
            link = f"https://www.youtube.com/watch?v={video_id}"
            songs.append((title, link))

    return songs

# ---------------- BUTTON ----------------
if st.button("🎧 Get Recommendations"):

    search_query = f"{language} {emotion} songs"

    st.subheader(f"🎵 {search_query.upper()}")

    songs = get_youtube_songs(search_query, 14)

    if not songs:
        st.warning("No songs found")
    else:
        random.shuffle(songs)

        for name, link in songs:
            st.markdown(f"""
            <div class="song-card">
                <h4 style='color:white'>{name}</h4>
            </div>
            """, unsafe_allow_html=True)

            st.video(link)
