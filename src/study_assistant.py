import re
import unicodedata
from collections import Counter


TOPICS = {
    "variables": {
        "keywords": ["variable", "variables", "dato", "datos", "asignacion", "tipo de dato"],
        "summary": "Una variable es un nombre que guarda un valor para usarlo despues en el programa.",
        "code": """nombre = "Sandra"
edad = 35
ciudad = "Buenos Aires"

print(nombre, edad, ciudad)""",
        "exercise": "Crea una variable con tu nombre, otra con tu edad y muestra ambas con `print`.",
    },
    "condicionales": {
        "keywords": ["if", "else", "elif", "condicion", "condicional", "decision"],
        "summary": "Un condicional permite ejecutar distintas instrucciones segun se cumpla o no una condicion.",
        "code": """edad = 18

if edad >= 18:
    print("Es mayor de edad")
else:
    print("Es menor de edad")""",
        "exercise": "Pide una edad por teclado e indica si la persona puede votar.",
    },
    "bucles": {
        "keywords": ["for", "while", "bucle", "ciclo", "iteracion", "repeticion"],
        "summary": "Un bucle sirve para repetir instrucciones sin escribir el mismo codigo muchas veces.",
        "code": """for numero in range(1, 6):
    print(numero)""",
        "exercise": "Muestra los numeros del 1 al 10 usando un bucle `for`.",
    },
    "listas": {
        "keywords": ["lista", "listas", "arreglo", "vector", "elementos", "append"],
        "summary": "Una lista guarda varios valores en una sola variable y permite recorrerlos, modificarlos o filtrarlos.",
        "code": """productos = ["notebook", "mouse", "teclado"]

for producto in productos:
    print(producto)""",
        "exercise": "Crea una lista con cinco herramientas de datos y muestra cada una con un bucle.",
    },
    "funciones": {
        "keywords": ["funcion", "funciones", "def", "parametro", "return", "retorno"],
        "summary": "Una funcion agrupa codigo reutilizable. Ayuda a ordenar el programa y evitar repetir instrucciones.",
        "code": """def saludar(nombre):
    return f"Hola, {nombre}"

mensaje = saludar("Sandra")
print(mensaje)""",
        "exercise": "Crea una funcion que reciba dos numeros y devuelva su suma.",
    },
    "algoritmos": {
        "keywords": ["algoritmo", "algoritmos", "problema", "solucion", "pasos", "logica"],
        "summary": "Un algoritmo es una serie ordenada de pasos para resolver un problema.",
        "code": """nota_1 = 8
nota_2 = 9
nota_3 = 7

promedio = (nota_1 + nota_2 + nota_3) / 3
print(promedio)""",
        "exercise": "Escribe los pasos para calcular el promedio de ventas de tres meses.",
    },
    "entrada_salida": {
        "keywords": ["input", "print", "entrada", "salida", "leer", "mostrar"],
        "summary": "`input` permite recibir datos del usuario y `print` permite mostrar resultados en pantalla.",
        "code": """nombre = input("Escribi tu nombre: ")
print(f"Hola, {nombre}")""",
        "exercise": "Pide al usuario su nombre y su ciudad, luego muestra una frase con ambos datos.",
    },
}


def normalize_text(text):
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    return "".join(char for char in text if unicodedata.category(char) != "Mn")


def find_topic(question):
    normalized_question = normalize_text(question)
    topic_scores = Counter()

    for topic, config in TOPICS.items():
        for keyword in config["keywords"]:
            normalized_keyword = normalize_text(keyword)
            if normalized_keyword in normalized_question:
                topic_scores[topic] += 3
            elif re.search(rf"\b{re.escape(normalized_keyword)}\b", normalized_question):
                topic_scores[topic] += 1

    return topic_scores.most_common(1)[0][0] if topic_scores else "algoritmos"


def wants_code(question):
    normalized_question = normalize_text(question)
    code_words = ["codigo", "linea", "ejemplo", "programa", "script", "sintaxis"]
    return any(word in normalized_question for word in code_words)


def build_study_response(question, pdf_path=None):
    topic = find_topic(question)
    config = TOPICS[topic]

    if wants_code(question):
        lead = "Claro. Un ejemplo simple seria:"
    else:
        lead = "Te lo explico de forma simple:"

    return (
        f"**Tema: {topic.replace('_', ' ')}**\n\n"
        f"{lead}\n\n"
        f"{config['summary']}\n\n"
        "```python\n"
        f"{config['code']}\n"
        "```\n\n"
        f"**Practica sugerida:** {config['exercise']}\n\n"
        "Podes pedirme otro ejemplo o un ejercicio mas dificil."
    )
