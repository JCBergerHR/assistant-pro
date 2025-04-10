import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, RTCConfiguration
import speech_recognition as sr
import av

# Configuration WebRTC avec serveur TURN public
RTC_CONFIGURATION = RTCConfiguration(
    {
        "iceServers": [
            {"urls": ["stun:stun.l.google.com:19302"]},
            {
                "urls": ["turn:openrelay.metered.ca:80"],
                "username": "openrelayproject",
                "credential": "openrelayproject"
            }
        ]
    }
)

st.set_page_config(page_title="Assistant Pro Démo", page_icon="🤖", layout="wide")

st.title("Assistant Pro de JC: Projet JARVIS")
st.write("Bienvenue dans votre assistant personnalisé !")

st.header("🎙️ Assistant vocal")
st.write("Clique sur Start pour activer le micro")

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.audio_text = ""

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        samples = frame.to_ndarray().flatten()
        audio_data = sr.AudioData(samples.tobytes(), frame.sample_rate, 2)
        try:
            text = self.recognizer.recognize_google(audio_data, language="fr-FR")
            self.audio_text = text
        except sr.UnknownValueError:
            pass  # Silencieusement ignorer les incompréhensions
        return frame

    def get_text(self):
        return self.audio_text

ctx = webrtc_streamer(
    key="speech",
    audio_processor_factory=AudioProcessor,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"audio": True, "video": False},
    async_processing=True,
)

if ctx.audio_processor:
    texte = ctx.audio_processor.get_text()
    if texte:
        st.success(f"🗣️ Vous avez dit : {texte}")
