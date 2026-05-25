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
AUTHOR_IMAGE_URL = "https://san-data.vercel.app/mailoyyo.jpeg"
PORTFOLIO_URL = "https://san-data.vercel.app/portfolio.html"
LINKEDIN_URL = "https://ar.linkedin.com/in/sandra-ortellado"
GITHUB_URL = "https://github.com/SanOrtellado"
sys.path.append(str(SRC_DIR))


st.set_page_config(
    page_title="Aprendizaje de algoritmos de Python | San-Data",
    page_icon=":speech_balloon:",
    layout="centered",
)


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


st.title("Aprendizaje de algoritmos de Python")
st.caption("by San-Data | Proyecto creado por Sandra Ortellado")

with st.sidebar:
    st.image(AUTHOR_IMAGE_URL, caption="Sandra Ortellado | San-Data")
    st.markdown("### Creado por Sandra Ortellado")
    st.markdown(
        "Analista de Datos, Lic. en Data Science en formacion y especialista en "
        "Growth Marketing & Research."
    )
    st.markdown("Transformo datos en decisiones inteligentes con Python, SQL y Power BI.")
    st.markdown(
        f"[Portfolio]({PORTFOLIO_URL}) | [LinkedIn]({LINKEDIN_URL}) | [GitHub]({GITHUB_URL})"
    )
    st.divider()

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
        else "Hola, soy el chatbot de San-Data. Preguntame sobre Python, IA, este proyecto o Sandra Ortellado."
    )
    st.session_state[message_key] = [
        {
            "role": "assistant",
            "content": intro,
        }
    ]

if mode == "Asistente de aprendizaje":
    if PDF_PATH.exists():
        st.success("Base de aprendizaje cargada.")
    else:
        st.info("Modo aprendizaje activo.")

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
