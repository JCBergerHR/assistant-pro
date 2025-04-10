import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import speech_recognition as sr
import av
import numpy as np

st.set_page_config(page_title="Assistant Pro Démo", page_icon="🤖", layout="wide")
st.title("Assistant Pro")
st.write("Bienvenue dans votre assistant personnalisé !")

st.header("🎙️ Assistant vocal")
st.write("Clique sur Start pour activer le micro")

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.audio_text = ""
        self.sample_rate = 16000  # Assuré pour Google API
        self.sample_width = 2     # 16 bits = 2 bytes

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        samples = frame.to_ndarray().flatten().astype(np.int16)
        audio_data = sr.AudioData(samples.tobytes(), self.sample_rate, self.sample_width)
        try:
            text = self.recognizer.recognize_google(audio_data, language="fr-FR")
            self.audio_text = text
        except sr.UnknownValueError:
            pass
        return frame

    def get_text(self):
        return self.audio_text

ctx = webrtc_streamer(
    key="speech",
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True, "video": False},
    async_processing=True,
)

if ctx and ctx.audio_processor:
    texte = ctx.audio_processor.get_text()
    if texte:
        st.success(f"🗣️ Vous avez dit : {texte}")
