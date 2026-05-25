import re
import unicodedata
from collections import Counter
from pathlib import Path

from pypdf import PdfReader


TOPICS = {
    "variables": {
        "keywords": ["variable", "variables", "dato", "datos", "asignacion", "tipo de dato"],
        "summary": "Las variables guardan valores para reutilizarlos durante la ejecucion de un programa.",
        "exercise": "Crea tres variables: nombre, edad y ciudad. Luego muestra una frase usando esos valores.",
    },
    "condicionales": {
        "keywords": ["if", "else", "elif", "condicion", "condicional", "decision"],
        "summary": "Los condicionales permiten que un programa tome decisiones segun una condicion verdadera o falsa.",
        "exercise": "Pide una edad por teclado e indica si la persona es menor o mayor de edad.",
    },
    "bucles": {
        "keywords": ["for", "while", "bucle", "ciclo", "iteracion", "repeticion"],
        "summary": "Los bucles ejecutan instrucciones varias veces, ya sea recorriendo elementos o repitiendo mientras se cumpla una condicion.",
        "exercise": "Muestra los numeros del 1 al 10 usando un bucle `for` y luego usando un bucle `while`.",
    },
    "listas": {
        "keywords": ["lista", "listas", "arreglo", "vector", "elementos", "append"],
        "summary": "Las listas permiten guardar varios valores en una sola estructura y recorrerlos o modificarlos.",
        "exercise": "Crea una lista con cinco productos y muestra cada producto con un bucle.",
    },
    "funciones": {
        "keywords": ["funcion", "funciones", "def", "parametro", "return", "retorno"],
        "summary": "Las funciones agrupan instrucciones reutilizables y ayudan a organizar mejor el codigo.",
        "exercise": "Crea una funcion `saludar(nombre)` que reciba un nombre y devuelva un saludo personalizado.",
    },
    "algoritmos": {
        "keywords": ["algoritmo", "algoritmos", "problema", "solucion", "pasos", "logica"],
        "summary": "Un algoritmo es una secuencia ordenada de pasos para resolver un problema.",
        "exercise": "Escribe en pseudocodigo los pasos para calcular el promedio de tres notas.",
    },
    "entrada_salida": {
        "keywords": ["input", "print", "entrada", "salida", "leer", "mostrar"],
        "summary": "La entrada permite recibir datos del usuario y la salida permite mostrar resultados.",
        "exercise": "Pide el nombre del usuario con `input` y muestra un mensaje de bienvenida con `print`.",
    },
}


def normalize_text(text):
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    return text


def extract_pages(pdf_path):
    reader = PdfReader(str(pdf_path))
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append({"page": page_number, "text": normalize_text(text)})

    return pages


def find_topic(question):
    normalized_question = normalize_text(question)
    topic_scores = Counter()

    for topic, config in TOPICS.items():
        for keyword in config["keywords"]:
            if normalize_text(keyword) in normalized_question:
                topic_scores[topic] += 3

    if topic_scores:
        return topic_scores.most_common(1)[0][0]

    for topic, config in TOPICS.items():
        for keyword in config["keywords"]:
            if re.search(rf"\b{re.escape(normalize_text(keyword))}\b", normalized_question):
                topic_scores[topic] += 1

    return topic_scores.most_common(1)[0][0] if topic_scores else "algoritmos"


def find_related_pages(pages, topic, limit=5):
    keywords = [normalize_text(keyword) for keyword in TOPICS[topic]["keywords"]]
    scored_pages = []

    for page in pages:
        score = sum(page["text"].count(keyword) for keyword in keywords)
        if score:
            scored_pages.append((score, page["page"]))

    scored_pages.sort(reverse=True)
    return [page_number for _, page_number in scored_pages[:limit]]


def build_study_response(question, pdf_path):
    if not Path(pdf_path).exists():
        return "No encontre el PDF en la carpeta del proyecto. Colocalo como `Algoritmos-resueltos-con-Python.pdf`."

    pages = extract_pages(pdf_path)
    topic = find_topic(question)
    related_pages = find_related_pages(pages, topic)
    config = TOPICS[topic]

    page_text = ", ".join(str(page) for page in related_pages) if related_pages else "no encontradas"

    return (
        f"Tema detectado: **{topic.replace('_', ' ')}**\n\n"
        f"Explicacion breve: {config['summary']}\n\n"
        f"Paginas sugeridas del PDF: {page_text}.\n\n"
        f"Ejercicio practico: {config['exercise']}\n\n"
        "Tip: preguntame por variables, condicionales, bucles, listas, funciones, entrada/salida o algoritmos."
    )
