import re
import unicodedata
from collections import Counter
from functools import lru_cache
from pathlib import Path

from pypdf import PdfReader


CONTENT_INDEX = [
    "Lenguaje de programacion Python",
    "Instalacion de Python y uso de VS Code",
    "Lenguaje y algoritmos",
    "Pseudocodigos y diagramas de flujo",
    "Identificadores, constantes y variables",
    "Operaciones aritmeticas, relacionales y logicas",
    "Instrucciones basicas: leer, asignar y escribir",
    "Estructuras selectivas",
    "Estructuras repetitivas: for, while y repetir",
    "Vectores y matrices",
]


PRACTICE_VARIANTS = {
    "python": [
        "Escribe un programa que muestre tu nombre, tu ciudad y una frase sobre lo que queres aprender.",
        "Crea un programa que imprima tres datos sobre vos en lineas separadas.",
        "Arma una presentacion en consola que combine texto fijo y variables.",
    ],
    "operaciones_aritmeticas": [
        "Calcula el subtotal, IVA y total de una compra usando operadores aritmeticos.",
        "Crea un programa que calcule el precio final despues de aplicar un descuento.",
        "Pide precio y cantidad por teclado, calcula subtotal, descuento, IVA y total final.",
    ],
    "operaciones_relacionales": [
        "Compara dos precios e indica cual es mayor.",
        "Compara dos edades y muestra si son iguales o diferentes.",
        "Crea un programa que compare tres ventas y determine si la primera supera a las otras dos.",
    ],
    "operaciones_logicas": [
        "Crea una condicion que valide si un usuario puede comprar: mayor de edad y saldo suficiente.",
        "Valida si una persona puede acceder a un beneficio usando dos condiciones combinadas.",
        "Crea un login simple que valide usuario correcto, clave correcta y cuenta activa.",
    ],
    "variables": [
        "Crea una variable con tu nombre, otra con tu edad y muestra ambas con `print`.",
        "Guarda producto, precio y cantidad en variables, luego muestra una frase con esos datos.",
        "Crea variables para una venta y calcula el total usando precio, cantidad y descuento.",
    ],
    "estructuras_repetitivas": [
        "Muestra los numeros del 1 al 10 y calcula su suma.",
        "Recorre una lista de ventas y muestra cada valor.",
        "Pide numeros hasta que el usuario escriba 0 y muestra la suma acumulada.",
    ],
    "for": [
        "Usa `for` para recorrer una lista de productos y mostrar cada uno.",
        "Usa `for` y `range` para mostrar la tabla del 5.",
        "Recorre una lista de ventas, calcula el total y cuenta cuantas superan 1000.",
    ],
    "while": [
        "Usa `while` para pedir una clave hasta que el usuario escriba la correcta.",
        "Usa `while` para contar del 1 al 10.",
        "Crea un menu que se repita hasta que el usuario elija la opcion salir.",
    ],
    "vectores": [
        "Crea un vector con ventas semanales y calcula el total y el promedio.",
        "Guarda cinco notas en una lista y muestra la nota mas alta.",
        "Recorre un vector de ventas y separa las ventas altas de las bajas.",
    ],
    "matrices": [
        "Crea una matriz de 2 filas por 3 columnas y muestra todos sus elementos con bucles anidados.",
        "Crea una matriz con ventas por sucursal y mes, luego muestra la primera fila.",
        "Calcula el total por fila de una matriz de ventas.",
    ],
}


STOPWORDS = {
    "a",
    "al",
    "algo",
    "como",
    "con",
    "de",
    "del",
    "dame",
    "el",
    "en",
    "es",
    "esta",
    "este",
    "genera",
    "hacer",
    "la",
    "las",
    "le",
    "lo",
    "los",
    "me",
    "para",
    "por",
    "que",
    "quiero",
    "se",
    "un",
    "una",
    "y",
}


SPECIFIC_EXERCISES = [
    {
        "keywords": ["precio", "final", "descuento"],
        "title": "precio final con descuento",
        "summary": "Para calcular el precio final se obtiene primero el descuento y luego se resta al precio original.",
        "pseudocode": """Inicio
    Leer precio
    Leer porcentaje_descuento
    descuento = precio * porcentaje_descuento / 100
    precio_final = precio - descuento
    Escribir precio_final
Fin""",
        "code": """precio = float(input("Precio original: "))
porcentaje_descuento = float(input("Descuento (%): "))

descuento = precio * porcentaje_descuento / 100
precio_final = precio - descuento

print(f"Descuento aplicado: {descuento}")
print(f"Precio final: {precio_final}")""",
        "exercise": "Agrega el calculo de IVA sobre el precio final con descuento.",
    },
    {
        "keywords": ["subtotal", "iva", "total", "compra"],
        "title": "subtotal, IVA y total de una compra",
        "summary": "El subtotal se calcula multiplicando precio por cantidad. Luego se calcula el IVA y se suma para obtener el total.",
        "pseudocode": """Inicio
    Leer precio
    Leer cantidad
    subtotal = precio * cantidad
    iva = subtotal * 0.21
    total = subtotal + iva
    Escribir subtotal
    Escribir iva
    Escribir total
Fin""",
        "code": """precio = float(input("Precio unitario: "))
cantidad = int(input("Cantidad: "))

subtotal = precio * cantidad
iva = subtotal * 0.21
total = subtotal + iva

print(f"Subtotal: {subtotal}")
print(f"IVA: {iva}")
print(f"Total: {total}")""",
        "exercise": "Agrega un descuento si el total supera 50000.",
    },
    {
        "keywords": ["area", "rectangulo"],
        "title": "area de un rectangulo",
        "summary": "Para calcular el area de un rectangulo se multiplica la base por la altura.",
        "pseudocode": """Inicio
    Leer base
    Leer altura
    area = base * altura
    Escribir area
Fin""",
        "code": """base = float(input("Base del rectangulo: "))
altura = float(input("Altura del rectangulo: "))

area = base * altura

print(f"El area del rectangulo es: {area}")""",
        "exercise": "Modifica el programa para calcular tambien el perimetro del rectangulo.",
    },
    {
        "keywords": ["promedio", "notas"],
        "title": "promedio de notas",
        "summary": "Para calcular un promedio se suman los valores y se dividen por la cantidad de datos.",
        "pseudocode": """Inicio
    Leer nota_1
    Leer nota_2
    Leer nota_3
    promedio = (nota_1 + nota_2 + nota_3) / 3
    Escribir promedio
Fin""",
        "code": """nota_1 = float(input("Primera nota: "))
nota_2 = float(input("Segunda nota: "))
nota_3 = float(input("Tercera nota: "))

promedio = (nota_1 + nota_2 + nota_3) / 3

print(f"El promedio es: {promedio}")""",
        "exercise": "Agrega una condicion para mostrar si el promedio es aprobado o desaprobado.",
    },
    {
        "keywords": ["promedio", "ventas", "meses"],
        "title": "promedio de ventas de tres meses",
        "summary": "Para calcular el promedio de ventas se suman las ventas de cada mes y se dividen por la cantidad de meses.",
        "pseudocode": """Inicio
    Leer venta_mes_1
    Leer venta_mes_2
    Leer venta_mes_3
    promedio = (venta_mes_1 + venta_mes_2 + venta_mes_3) / 3
    Escribir promedio
Fin""",
        "code": """venta_mes_1 = float(input("Venta mes 1: "))
venta_mes_2 = float(input("Venta mes 2: "))
venta_mes_3 = float(input("Venta mes 3: "))

promedio = (venta_mes_1 + venta_mes_2 + venta_mes_3) / 3

print(f"Promedio de ventas: {promedio}")""",
        "exercise": "Agrega una condicion que indique si el promedio supera el objetivo comercial.",
    },
    {
        "keywords": ["nombre", "ciudad", "frase", "aprender"],
        "title": "presentacion personal en Python",
        "summary": "Este programa guarda datos personales en variables y los muestra en pantalla usando `print`.",
        "pseudocode": """Inicio
    nombre = "Sandra"
    ciudad = "Buenos Aires"
    objetivo = "aprender algoritmos con Python"
    Escribir nombre
    Escribir ciudad
    Escribir objetivo
Fin""",
        "code": """nombre = "Sandra"
ciudad = "Buenos Aires"
objetivo = "aprender algoritmos con Python"

print(f"Mi nombre es {nombre}")
print(f"Vivo en {ciudad}")
print(f"Quiero {objetivo}")""",
        "exercise": "Modifica el programa para pedir esos datos con `input`.",
    },
    {
        "keywords": ["mayor", "menor", "edad"],
        "title": "validar mayoria de edad",
        "summary": "Este algoritmo usa una estructura selectiva para decidir segun la edad ingresada.",
        "pseudocode": """Inicio
    Leer edad
    Si edad >= 18 Entonces
        Escribir "Es mayor de edad"
    SiNo
        Escribir "Es menor de edad"
    FinSi
Fin""",
        "code": """edad = int(input("Edad: "))

if edad >= 18:
    print("Es mayor de edad")
else:
    print("Es menor de edad")""",
        "exercise": "Agrega una segunda condicion para indicar si la persona tambien puede votar.",
    },
]


TOPICS = {
    "python": {
        "keywords": ["python", "lenguaje", "programacion", "caracteristicas", "por que python"],
        "summary": "Python es un lenguaje de programacion claro, flexible y muy usado para automatizacion, datos, inteligencia artificial, web y educacion.",
        "code": """print("Mi primer programa en Python")""",
        "exercise": "Escribe un programa que muestre tu nombre, tu ciudad y una frase sobre lo que queres aprender.",
    },
    "instalacion_python": {
        "keywords": ["instalar python", "instalacion", "cmd", "terminal", "interprete", "version python"],
        "summary": "Para trabajar con Python se instala el interprete, se verifica desde la terminal y luego se ejecutan archivos `.py`.",
        "code": """# Comandos utiles en terminal
python --version
python archivo.py""",
        "exercise": "Crea un archivo `saludo.py`, escribe un `print` y ejecutalo desde la terminal.",
    },
    "vscode": {
        "keywords": ["visual studio code", "vscode", "vs code", "extension", "plugin", "atajos"],
        "summary": "VS Code es un editor muy usado para programar en Python porque permite abrir carpetas, ejecutar archivos, usar terminal integrada e instalar extensiones.",
        "code": """# Flujo tipico
# 1. Abrir carpeta del proyecto
# 2. Crear archivo app.py
# 3. Ejecutar:
python app.py""",
        "exercise": "Abre una carpeta en VS Code, crea `main.py` y ejecuta un programa simple desde la terminal integrada.",
    },
    "algoritmos": {
        "keywords": ["algoritmo", "algoritmos", "problema", "solucion", "pasos", "logica"],
        "summary": "Un algoritmo es una secuencia ordenada de pasos para resolver un problema. Antes de programar, conviene pensar entradas, proceso y salida.",
        "code": """nota_1 = 8
nota_2 = 9
nota_3 = 7

promedio = (nota_1 + nota_2 + nota_3) / 3
print(promedio)""",
        "exercise": "Escribe los pasos para calcular el promedio de ventas de tres meses y luego pasalo a Python.",
    },
    "pseudocodigo": {
        "keywords": ["pseudocodigo", "pseudocodigos", "pseudo", "partes del pseudocodigo"],
        "summary": "El pseudocodigo describe la logica de un algoritmo con lenguaje cercano al humano, antes de escribir codigo real.",
        "code": """# Pseudocodigo:
# Leer precio
# Leer cantidad
# total = precio * cantidad
# Escribir total

precio = 1500
cantidad = 3
total = precio * cantidad
print(total)""",
        "exercise": "Escribe en pseudocodigo un algoritmo para calcular el area de un rectangulo y luego implementalo en Python.",
    },
    "diagramas": {
        "keywords": ["diagrama", "diagramas", "flujo", "simbolos", "carta n-s", "nassi"],
        "summary": "Un diagrama de flujo representa visualmente un algoritmo usando simbolos para inicio, entrada, proceso, decision y salida.",
        "code": """# Ejemplo de decision que podria representarse en un diagrama
edad = 20

if edad >= 18:
    print("Puede ingresar")
else:
    print("No puede ingresar")""",
        "exercise": "Dibuja el flujo para decidir si una nota es aprobada o desaprobada y luego escribilo con `if`.",
    },
    "identificadores": {
        "keywords": ["identificador", "identificadores", "nombre variable", "nombres", "reglas"],
        "summary": "Un identificador es el nombre que se le da a variables, funciones u otros elementos. Debe ser claro, descriptivo y no usar palabras reservadas.",
        "code": """nombre_cliente = "Ana"
total_ventas = 25000
es_activo = True""",
        "exercise": "Crea cinco nombres de variables descriptivos para un sistema de ventas.",
    },
    "constantes": {
        "keywords": ["constante", "constantes", "valor fijo"],
        "summary": "Una constante representa un valor que conceptualmente no deberia cambiar durante la ejecucion del programa.",
        "code": """IVA = 0.21
precio = 1000
precio_final = precio * (1 + IVA)

print(precio_final)""",
        "exercise": "Define una constante `DESCUENTO` y usala para calcular el precio final de un producto.",
    },
    "variables": {
        "keywords": ["variable", "variables", "dato", "datos", "asignacion", "tipo de dato"],
        "summary": "Una variable es un nombre que guarda un valor para usarlo despues en el programa.",
        "code": """nombre = "Sandra"
edad = 35
ciudad = "Buenos Aires"

print(nombre, edad, ciudad)""",
        "exercise": "Crea una variable con tu nombre, otra con tu edad y muestra ambas con `print`.",
    },
    "operaciones_aritmeticas": {
        "keywords": ["aritmetica", "aritmeticas", "suma", "resta", "multiplicacion", "division", "modulo", "operadores aritmeticos"],
        "summary": "Las operaciones aritmeticas permiten realizar calculos matematicos como suma, resta, multiplicacion, division, potencia y modulo.",
        "code": """a = 10
b = 3

print(a + b)
print(a - b)
print(a * b)
print(a / b)
print(a % b)""",
        "exercise": "Calcula el subtotal, IVA y total de una compra usando operadores aritmeticos.",
    },
    "operaciones_relacionales": {
        "keywords": ["relacional", "relacionales", "mayor", "menor", "igual", "comparacion", "comparar"],
        "summary": "Las operaciones relacionales comparan valores y devuelven `True` o `False`.",
        "code": """edad = 21

print(edad >= 18)
print(edad == 21)
print(edad != 30)""",
        "exercise": "Compara dos precios e indica cual es mayor.",
    },
    "operaciones_logicas": {
        "keywords": ["logica", "logicas", "and", "or", "not", "operadores logicos"],
        "summary": "Las operaciones logicas combinan condiciones. En Python se usan `and`, `or` y `not`.",
        "code": """edad = 25
tiene_permiso = True

if edad >= 18 and tiene_permiso:
    print("Acceso permitido")""",
        "exercise": "Crea una condicion que valide si un usuario puede comprar: mayor de edad y saldo suficiente.",
    },
    "leer": {
        "keywords": ["leer", "input", "entrada", "capturar dato", "pedir dato"],
        "summary": "Leer datos significa recibir informacion del usuario. En Python se usa `input`.",
        "code": """nombre = input("Escribi tu nombre: ")
print(f"Hola, {nombre}")""",
        "exercise": "Pide el nombre y edad del usuario, luego muestra un mensaje personalizado.",
    },
    "asignar": {
        "keywords": ["asignar", "asignacion", "guardar valor"],
        "summary": "Asignar es guardar un valor dentro de una variable usando el signo `=`.",
        "code": """precio = 1200
cantidad = 4
total = precio * cantidad

print(total)""",
        "exercise": "Asigna valores a precio y cantidad, calcula el total y muestralo.",
    },
    "escribir": {
        "keywords": ["escribir", "mostrar", "salida", "print", "imprimir"],
        "summary": "Escribir o mostrar datos significa presentar informacion en pantalla. En Python se usa `print`.",
        "code": """mensaje = "Aprendiendo algoritmos con Python"
print(mensaje)""",
        "exercise": "Muestra en pantalla tres mensajes: nombre del programa, autora y objetivo.",
    },
    "estructuras_selectivas": {
        "keywords": ["selectiva", "selectivas", "if", "else", "elif", "condicional", "decision"],
        "summary": "Las estructuras selectivas permiten tomar decisiones y ejecutar caminos distintos segun una condicion.",
        "code": """nota = 8

if nota >= 7:
    print("Aprobado")
elif nota >= 4:
    print("Regular")
else:
    print("Desaprobado")""",
        "exercise": "Crea un programa que clasifique una compra como baja, media o alta segun su importe.",
    },
    "estructuras_repetitivas": {
        "keywords": ["repetitiva", "repetitivas", "bucle", "ciclo", "for", "while", "repetir"],
        "summary": "Las estructuras repetitivas ejecutan instrucciones varias veces. En Python las mas usadas son `for` y `while`.",
        "code": """for numero in range(1, 6):
    print(numero)""",
        "exercise": "Muestra los numeros del 1 al 10 y calcula su suma.",
    },
    "for": {
        "keywords": ["for", "para", "desde", "range"],
        "summary": "`for` se usa cuando queremos recorrer una secuencia o repetir una accion una cantidad conocida de veces.",
        "code": """for i in range(1, 6):
    print(f"Vuelta {i}")""",
        "exercise": "Usa `for` para recorrer una lista de productos y mostrar cada uno.",
    },
    "while": {
        "keywords": ["while", "mientras"],
        "summary": "`while` repite instrucciones mientras una condicion sea verdadera.",
        "code": """contador = 1

while contador <= 5:
    print(contador)
    contador += 1""",
        "exercise": "Usa `while` para pedir una clave hasta que el usuario escriba la correcta.",
    },
    "repetir": {
        "keywords": ["repetir", "repeat", "hasta que"],
        "summary": "La estructura `repetir` ejecuta al menos una vez y luego evalua una condicion de salida. En Python se puede simular con `while True` y `break`.",
        "code": """while True:
    clave = input("Clave: ")
    if clave == "python":
        break

print("Acceso correcto")""",
        "exercise": "Crea un programa que pida un numero positivo y repita hasta recibir uno valido.",
    },
    "vectores": {
        "keywords": ["vector", "vectores", "array unidimensional", "arreglo", "lista"],
        "summary": "Un vector almacena varios elementos en una sola dimension. En Python se puede representar con una lista.",
        "code": """ventas = [1200, 1500, 1800, 1300]
total = sum(ventas)

print(total)""",
        "exercise": "Crea un vector con ventas semanales y calcula el total y el promedio.",
    },
    "matrices": {
        "keywords": ["matriz", "matrices", "array multidimensional", "bidimensional", "tabla"],
        "summary": "Una matriz organiza datos en filas y columnas. En Python puede representarse como una lista de listas.",
        "code": """matriz = [
    [1, 2, 3],
    [4, 5, 6],
]

print(matriz[0][1])""",
        "exercise": "Crea una matriz de 2 filas por 3 columnas y muestra todos sus elementos con bucles anidados.",
    },
}


def normalize_text(text):
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    return "".join(char for char in text if unicodedata.category(char) != "Mn")


def extract_query_terms(question):
    normalized_question = normalize_text(question)
    terms = re.findall(r"[a-z0-9_]+", normalized_question)
    return [term for term in terms if len(term) > 2 and term not in STOPWORDS]


@lru_cache(maxsize=2)
def load_learning_material(pdf_path):
    path = Path(pdf_path) if pdf_path else None
    if not path or not path.exists():
        return []

    reader = PdfReader(str(path))
    chunks = []

    for page in reader.pages:
        text = normalize_text(page.extract_text() or "")
        paragraphs = [paragraph.strip() for paragraph in re.split(r"\n{2,}|\r\n{2,}", text) if paragraph.strip()]
        chunks.extend(paragraphs)

    return chunks


def search_learning_material(question, pdf_path, limit=5):
    terms = extract_query_terms(question)
    if not terms:
        return []

    matches = []
    for chunk in load_learning_material(str(pdf_path)):
        score = sum(chunk.count(term) for term in terms)
        if score:
            matches.append((score, chunk))

    matches.sort(key=lambda item: item[0], reverse=True)
    return [chunk for _, chunk in matches[:limit]]


def score_topics_from_text(text):
    scores = Counter()
    normalized_text = normalize_text(text)

    for topic, config in TOPICS.items():
        for keyword in config["keywords"]:
            normalized_keyword = normalize_text(keyword)
            if normalized_keyword in normalized_text:
                scores[topic] += 1

    return scores


def find_topic(question, pdf_path=None):
    normalized_question = normalize_text(question)
    topic_scores = Counter()

    for topic, config in TOPICS.items():
        for keyword in config["keywords"]:
            normalized_keyword = normalize_text(keyword)
            if normalized_keyword in normalized_question:
                topic_scores[topic] += 2 + (len(normalized_keyword.split()) * 2)
            elif re.search(rf"\b{re.escape(normalized_keyword)}\b", normalized_question):
                topic_scores[topic] += 1

    if pdf_path:
        material_matches = search_learning_material(question, pdf_path)
        material_text = " ".join(material_matches)
        for topic, score in score_topics_from_text(material_text).items():
            topic_scores[topic] += score

    return topic_scores.most_common(1)[0][0] if topic_scores else "algoritmos"


def asks_for_index(question):
    normalized_question = normalize_text(question)
    triggers = ["contenido", "indice", "temario", "temas", "que puedo aprender", "que sabes"]
    return any(trigger in normalized_question for trigger in triggers)


def wants_code(question):
    normalized_question = normalize_text(question)
    code_words = ["codigo", "linea", "ejemplo", "programa", "script", "sintaxis"]
    return any(word in normalized_question for word in code_words)


def wants_harder_practice(question):
    normalized_question = normalize_text(question)
    triggers = ["dificil", "avanzado", "desafio", "mas complejo", "nivel mas"]
    return any(trigger in normalized_question for trigger in triggers)


def wants_another_practice(question):
    normalized_question = normalize_text(question)
    triggers = ["otro", "otra", "distinto", "diferente", "nuevo", "nueva"]
    return any(trigger in normalized_question for trigger in triggers)


def get_practice(topic, question):
    practices = PRACTICE_VARIANTS.get(topic)
    if not practices:
        return TOPICS[topic]["exercise"]

    if wants_harder_practice(question):
        return practices[-1]

    if wants_another_practice(question):
        return practices[1] if len(practices) > 1 else practices[0]

    return practices[0]


def find_specific_exercise(question):
    normalized_question = normalize_text(question)

    for exercise in SPECIFIC_EXERCISES:
        if all(keyword in normalized_question for keyword in exercise["keywords"]):
            return exercise

    return None


def build_specific_exercise_response(exercise):
    return (
        f"**Ejercicio: {exercise['title']}**\n\n"
        f"{exercise['summary']}\n\n"
        "**Pseudocodigo**\n\n"
        "```text\n"
        f"{exercise['pseudocode']}\n"
        "```\n\n"
        "**Implementacion en Python**\n\n"
        "```python\n"
        f"{exercise['code']}\n"
        "```\n\n"
        f"**Desafio extra:** {exercise['exercise']}"
    )


def build_index_response():
    items = "\n".join(f"- {item}" for item in CONTENT_INDEX)
    return (
        "**Temario disponible**\n\n"
        f"{items}\n\n"
        "Podes pedirme conceptos, ejemplos de codigo o ejercicios sobre cualquiera de estos temas."
    )


def build_study_response(question, pdf_path=None):
    if asks_for_index(question):
        return build_index_response()

    specific_exercise = find_specific_exercise(question)
    if specific_exercise:
        return build_specific_exercise_response(specific_exercise)

    topic = find_topic(question, pdf_path)
    config = TOPICS[topic]
    lead = "Claro. Un ejemplo simple seria:" if wants_code(question) else "Te lo explico de forma simple:"
    practice = get_practice(topic, question)

    return (
        f"**Tema: {topic.replace('_', ' ')}**\n\n"
        f"{lead}\n\n"
        f"{config['summary']}\n\n"
        "```python\n"
        f"{config['code']}\n"
        "```\n\n"
        f"**Practica sugerida:** {practice}\n\n"
        "Podes pedirme otro ejemplo, un ejercicio mas dificil o el temario completo."
    )
