import sys
from pathlib import Path

import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
sys.path.append(str(SRC_DIR))

from chatbot import get_response, load_resources, predict_class  # noqa: E402


st.set_page_config(page_title="Chatbot con Python", page_icon="Chat", layout="centered")


@st.cache_resource
def cached_resources():
    return load_resources()


def render_message(role, text):
    with st.chat_message(role):
        st.write(text)


st.title("Chatbot con Python")
st.caption("Demo interactiva entrenada con NLTK, TensorFlow/Keras y un dataset de intenciones.")

model_path = BASE_DIR / "model" / "chatbot_model.keras"

if not model_path.exists():
    st.warning("Primero entrena el modelo desde la terminal con `python src/train.py`.")
    st.stop()

intents, words, classes, model = cached_resources()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hola, soy tu chatbot. Preguntame sobre Python, IA o este proyecto.",
        }
    ]

for message in st.session_state.messages:
    render_message(message["role"], message["content"])

prompt = st.chat_input("Escribi tu mensaje...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    render_message("user", prompt)

    predicted = predict_class(prompt, model, words, classes)
    response = get_response(predicted, intents)

    st.session_state.messages.append({"role": "assistant", "content": response})
    render_message("assistant", response)
