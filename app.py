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


def render_header():
    st.markdown(
        """
        <div style="padding: 0.75rem 0 1.25rem 0; border-bottom: 1px solid rgba(255,255,255,0.12); margin-bottom: 1.5rem;">
            <strong>San-Data</strong> · Aprendizaje de algoritmos de Python
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    st.markdown(
        """
        <div style="padding-top: 2rem; margin-top: 2rem; border-top: 1px solid rgba(255,255,255,0.12); opacity: 0.75;">
            Proyecto educativo creado por Sandra Ortellado · San-Data
        </div>
        """,
        unsafe_allow_html=True,
    )


def select_mode(mode_name):
    st.session_state.active_mode = mode_name
    st.session_state.show_home = False


def go_home():
    st.session_state.show_home = True


def render_home():
    st.title("Aprendizaje de algoritmos de Python")
    st.caption("by San-Data | Proyecto creado por Sandra Ortellado")
    st.markdown("### Elegi como queres aprender")

    mode_col_1, mode_col_2, mode_col_3 = st.columns(3)

    with mode_col_1:
        if st.button("Asistente de aprendizaje", use_container_width=True):
            select_mode("Asistente de aprendizaje")
            st.rerun()

    with mode_col_2:
        if st.button("Practica guiada", use_container_width=True):
            select_mode("Practica guiada")
            st.rerun()

    with mode_col_3:
        if st.button("Ruta de aprendizaje", use_container_width=True):
            select_mode("Ruta de aprendizaje")
            st.rerun()

    st.link_button("Ver perfil San-Data", PORTFOLIO_URL, use_container_width=True)
    st.caption(
        "El asistente responde dudas con conceptos y codigo. La practica guiada propone desafios con feedback inmediato."
    )


render_header()

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

mode_options = ["Asistente de aprendizaje", "Practica guiada", "Ruta de aprendizaje"]

if "active_mode" not in st.session_state:
    st.session_state.active_mode = "Asistente de aprendizaje"
if "show_home" not in st.session_state:
    st.session_state.show_home = True

mode = st.sidebar.radio(
    "Modo",
    mode_options,
    index=mode_options.index(st.session_state.active_mode),
)
st.session_state.active_mode = mode

ml_ready = MODEL_PATH.exists()
resources = None

if ml_ready:
    try:
        resources = load_ml_resources()
    except ModuleNotFoundError:
        ml_ready = False

mode = st.session_state.active_mode

if not st.session_state.show_home:
    if st.button("Volver a Home", key="top_home"):
        go_home()
        st.rerun()

if st.session_state.show_home:
    render_home()
    render_footer()
    st.stop()

if mode == "Asistente de aprendizaje":
    st.info("Modo aprendizaje activo: pregunta por temas, codigo, ejercicios o temario completo.")

if mode == "Ruta de aprendizaje":
    from learning_path import get_lesson, total_lessons, validate_answer

    if "path_index" not in st.session_state:
        st.session_state.path_index = 0
    if "path_xp" not in st.session_state:
        st.session_state.path_xp = 0
    if "path_streak" not in st.session_state:
        st.session_state.path_streak = 1
    if "path_answered" not in st.session_state:
        st.session_state.path_answered = False

    lesson = get_lesson(st.session_state.path_index)
    progress = (st.session_state.path_index + 1) / total_lessons()

    st.subheader(f"Seccion: {lesson['section']}")
    st.caption(f"Racha diaria: {st.session_state.path_streak} dia | XP: {st.session_state.path_xp}/100")
    st.progress(progress)

    st.markdown(f"### {st.session_state.path_index + 1:02d}. {lesson['title']}")
    st.write(lesson["goal"])
    st.info(lesson["lesson"])

    st.markdown("#### script.py")
    answer = st.text_area(
        lesson["prompt"],
        value=lesson["starter"] if st.session_state.path_answered else "",
        height=120,
        key=f"path_answer_{st.session_state.path_index}",
        disabled=st.session_state.path_answered,
    )

    if st.button("Comprobar", disabled=st.session_state.path_answered):
        is_correct = validate_answer(lesson, answer)
        st.session_state.path_answered = True
        st.session_state.path_is_correct = is_correct
        if is_correct:
            st.session_state.path_xp += 10
        st.rerun()

    if st.session_state.path_answered:
        if st.session_state.path_is_correct:
            st.success(f"Leccion resuelta. +10 XP. {lesson['feedback']}")
        else:
            st.error("Todavia no. Revisa el nombre de la variable, el signo `=` o la sintaxis.")
            st.code(lesson["starter"], language="python")

        col_continue, col_home = st.columns(2)
        with col_continue:
            if st.button("Continuar", key="path_continue"):
                st.session_state.path_index = (st.session_state.path_index + 1) % total_lessons()
                st.session_state.path_answered = False
                st.session_state.path_is_correct = False
                st.rerun()
        with col_home:
            if st.button("Volver a Home", key="path_home"):
                go_home()
                st.rerun()

    if st.button("Reiniciar ruta"):
        st.session_state.path_index = 0
        st.session_state.path_xp = 0
        st.session_state.path_streak = 1
        st.session_state.path_answered = False
        st.session_state.path_is_correct = False
        st.rerun()

    render_footer()
    st.stop()

if mode == "Practica guiada":
    from guided_practice import get_question, total_questions

    if "practice_index" not in st.session_state:
        st.session_state.practice_index = 0
    if "practice_answered" not in st.session_state:
        st.session_state.practice_answered = False
    if "practice_score" not in st.session_state:
        st.session_state.practice_score = 0

    question = get_question(st.session_state.practice_index)
    progress = (st.session_state.practice_index + 1) / total_questions()

    st.subheader(f"Practica guiada: {question['topic']}")
    st.progress(progress)
    st.caption(
        f"Pregunta {st.session_state.practice_index + 1} de {total_questions()} | "
        f"Puntaje: {st.session_state.practice_score}"
    )

    st.markdown(f"### {question['question']}")

    selected_option = st.radio(
        "Elegi una respuesta",
        question["options"],
        key=f"practice_option_{st.session_state.practice_index}",
        disabled=st.session_state.practice_answered,
    )

    if st.button("Responder", disabled=st.session_state.practice_answered):
        selected_index = question["options"].index(selected_option)
        st.session_state.practice_answered = True
        st.session_state.practice_is_correct = selected_index == question["answer"]
        if st.session_state.practice_is_correct:
            st.session_state.practice_score += 1
        st.rerun()

    if st.session_state.practice_answered:
        if st.session_state.practice_is_correct:
            st.success(question["feedback_ok"])
        else:
            st.error(question["feedback_bad"])

        st.info(question["mini_lesson"])

        col_continue, col_home = st.columns(2)
        with col_continue:
            if st.button("Continuar", key="practice_continue"):
                st.session_state.practice_index = (
                    st.session_state.practice_index + 1
                ) % total_questions()
                st.session_state.practice_answered = False
                st.session_state.practice_is_correct = False
                st.rerun()
        with col_home:
            if st.button("Volver a Home", key="practice_home"):
                go_home()
                st.rerun()

    if st.button("Reiniciar practica"):
        st.session_state.practice_index = 0
        st.session_state.practice_answered = False
        st.session_state.practice_score = 0
        st.session_state.practice_is_correct = False
        st.rerun()

    render_footer()
    st.stop()

message_key = "study_messages"

if message_key not in st.session_state:
    intro = (
        "Hola, soy tu asistente de aprendizaje. Preguntame por temas como bucles, listas, funciones o condicionales."
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
    else:
        response = demo_response(prompt, load_demo_intents())

    st.session_state[message_key].append({"role": "assistant", "content": response})
    render_message("assistant", response)

render_footer()
