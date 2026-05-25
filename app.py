import json
import random
import sys
from difflib import SequenceMatcher
from pathlib import Path

import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
DATA_PATH = BASE_DIR / "data" / "intents.json"
MODEL_PATH = BASE_DIR / "model" / "chatbot_model.keras"
PDF_PATH = BASE_DIR / "Algoritmos-resueltos-con-Python.pdf"
sys.path.append(str(SRC_DIR))


st.set_page_config(page_title="Chatbot con Python", page_icon=":speech_balloon:", layout="centered")


@st.cache_resource
def load_ml_resources():
    from chatbot import get_response, load_resources, predict_class

    intents, words, classes, model = load_resources()
    return intents, words, classes, model, get_response, predict_class


@st.cache_data
def load_demo_intents():
    with DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def similarity(first_text, second_text):
    return SequenceMatcher(None, first_text.lower(), second_text.lower()).ratio()


def demo_response(message, intents):
    best_score = 0
    best_intent = None

    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            score = similarity(message, pattern)
            if score > best_score:
                best_score = score
                best_intent = intent

    if best_intent and best_score >= 0.35:
        return random.choice(best_intent["responses"])

    return "No estoy seguro de haber entendido. Podrias escribirlo de otra forma?"


def render_message(role, text):
    with st.chat_message(role):
        st.markdown(text)


st.title("Chatbot con Python")
st.caption("Demo interactiva con dataset de intenciones, NLTK y TensorFlow/Keras.")

mode = st.sidebar.radio(
    "Modo",
    ["Chatbot general", "Asistente de aprendizaje"],
)

ml_ready = MODEL_PATH.exists()
resources = None

if ml_ready:
    try:
        resources = load_ml_resources()
    except ModuleNotFoundError:
        ml_ready = False

if ml_ready and resources:
    st.success("Modo modelo entrenado activo.")
else:
    st.info("Modo demo activo. Para usar la red neuronal, instala TensorFlow con Python 3.10, 3.11 o 3.12 y entrena el modelo.")

message_key = "study_messages" if mode == "Asistente de aprendizaje" else "chat_messages"

if message_key not in st.session_state:
    intro = (
        "Hola, soy tu asistente de aprendizaje. Preguntame por temas como bucles, listas, funciones o condicionales."
        if mode == "Asistente de aprendizaje"
        else "Hola, soy tu chatbot. Preguntame sobre Python, IA o este proyecto."
    )
    st.session_state[message_key] = [
        {
            "role": "assistant",
            "content": intro,
        }
    ]

if mode == "Asistente de aprendizaje":
    if PDF_PATH.exists():
        st.success("PDF cargado: Algoritmos-resueltos-con-Python.pdf")
    else:
        st.warning("No encontre el PDF en la carpeta del proyecto.")

for message in st.session_state[message_key]:
    render_message(message["role"], message["content"])

prompt = st.chat_input("Escribi tu mensaje...")

if prompt:
    st.session_state[message_key].append({"role": "user", "content": prompt})
    render_message("user", prompt)

    if mode == "Asistente de aprendizaje":
        from study_assistant import build_study_response

        response = build_study_response(prompt, PDF_PATH)
    elif ml_ready and resources:
        intents, words, classes, model, get_response, predict_class = resources
        predicted = predict_class(prompt, model, words, classes)
        response = get_response(predicted, intents)
    else:
        response = demo_response(prompt, load_demo_intents())

    st.session_state[message_key].append({"role": "assistant", "content": response})
    render_message("assistant", response)
