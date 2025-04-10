import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import speech_recognition as sr
import av

st.set_page_config(page_title="Assistant Pro Démo", page_icon="🤖", layout="wide")

st.title("Assistant Pro")
st.write("Bienvenue dans votre assistant personnalisé !")

st.header("🎙️ Assistant vocal")
st.write("Clique sur Start pour activer le micro")

# Configuration et activation du micro
webrtc_streamer(
    key="speech",
    client_settings=ClientSettings(
        media_stream_constraints={"audio": True, "video": False},
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )
)
