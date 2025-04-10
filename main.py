import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, ClientSettings
import speech_recognition as sr
import av

# Configuration de la page
st.set_page_config(page_title="Assistant Pro de JC: Projet JARVIS", page_icon="🤖", layout="wide")

st.title("Assistant Pro de JC: Projet JARVIS")
st.write("Bienvenue dans votre assistant personnalisé !")

# Section assistant vocal
st.header("🎙️ Assistant vocal")
st.write("Clique sur Start pour activer le micro")

# Classe pour le traitement audio
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
            pass  # Silencieusement ignorer les erreurs
        return frame

    def get_text(self):
        return self.audio_text

# Configuration du client WebRTC avec TURN server (utile derrière VPN)
client_settings = ClientSettings(
    rtc_configuration={
        "iceServers": [
            {"urls": ["stun:stun.l.google.com:19302"]},
            {
                "urls": ["turn:openrelay.metered.ca:80"],
                "username": "openrelayproject",
                "credential": "openrelayproject",
            },
        ]
    },
    media_stream_constraints={"audio": True, "video": False},
)

# Lancement du streamer WebRTC
ctx = webrtc_streamer(
    key="speech",
    audio_processor_factory=AudioProcessor,
    client_settings=client_settings,
    async_processing=True,
)

# Affichage du texte transcrit
if ctx.audio_processor:
    texte = ctx.audio_processor.get_text()
    if texte:
        st.success(f"🗣️ Vous avez dit : {texte}")
