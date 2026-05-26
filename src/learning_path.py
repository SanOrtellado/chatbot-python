import re


LESSONS = [
    {
        "title": "Creacion de variables",
        "section": "Introduccion a Python",
        "goal": "Crea variables que almacenen texto y numeros.",
        "lesson": "Una variable guarda un valor para usarlo despues. En Python se crea con un nombre, el signo `=` y un valor.",
        "prompt": "Ahora crea una variable diferente llamada `favorite_language` con el valor `Python`.",
        "example": 'user_name = "Sandra"',
        "hint": 'Recorda usar snake_case y comillas para textos: `favorite_language = "Python"`.',
        "starter": 'favorite_language = "Python"',
        "validator": "favorite_language",
        "feedback": "Excelente. Creaste una variable nueva usando snake_case y guardaste texto.",
    },
    {
        "title": "Uso de variables",
        "section": "Introduccion a Python",
        "goal": "Usa una variable dentro de una salida.",
        "lesson": "Despues de crear una variable, podes mostrarla en pantalla con `print()`.",
        "prompt": "Muestra la variable `home_city` usando `print()`.",
        "example": "print(user_name)",
        "hint": "No pongas comillas alrededor de `home_city`, porque queres mostrar la variable.",
        "starter": "print(home_city)",
        "validator": "print_home_city",
        "feedback": "Bien. `print(home_city)` muestra el valor guardado en la variable.",
    },
    {
        "title": "Verdadero y falso",
        "section": "Introduccion a Python",
        "goal": "Reconoce valores booleanos.",
        "lesson": "`True` y `False` representan verdadero y falso. Se usan mucho en condiciones.",
        "prompt": "Crea una variable `is_learning` con el valor `True`.",
        "example": "is_active = True",
        "hint": "`True` empieza con mayuscula en Python.",
        "starter": "is_learning = True",
        "validator": "is_learning",
        "feedback": "Correcto. `True` es un valor booleano.",
    },
    {
        "title": "Comparacion numerica",
        "section": "Introduccion a Python",
        "goal": "Compara dos numeros.",
        "lesson": "Los operadores relacionales comparan valores y devuelven `True` o `False`.",
        "prompt": "Comprueba si `edad` es mayor o igual a 18.",
        "example": "precio >= 1000",
        "hint": "Mayor o igual se escribe con el operador `>=`.",
        "starter": "edad >= 18",
        "validator": "edad_compare",
        "feedback": "Muy bien. `>=` evalua si un valor es mayor o igual que otro.",
    },
    {
        "title": "Formato de cadenas",
        "section": "Introduccion a Python",
        "goal": "Combina texto y variables.",
        "lesson": "Las f-strings permiten insertar variables dentro de un texto.",
        "prompt": "Crea una frase con la variable `nombre` usando una f-string.",
        "example": 'f"Bienvenida, {user_name}"',
        "hint": "Una f-string empieza con `f` y usa llaves `{}` para insertar variables.",
        "starter": 'f"Hola, {nombre}"',
        "validator": "f_string",
        "feedback": "Genial. Las f-strings hacen que el texto con variables sea mas legible.",
    },
    {
        "title": "Proyecto Bot",
        "section": "Proyecto guiado",
        "goal": "Prepara una respuesta simple de un bot.",
        "lesson": "Un bot puede responder guardando mensajes y mostrando una salida.",
        "prompt": "Crea una variable `bot_response` con un saludo.",
        "example": 'message = "Hola, bienvenida"',
        "hint": "La variable debe llamarse `bot_response` y guardar un texto entre comillas.",
        "starter": 'bot_response = "Hola, soy tu bot"',
        "validator": "bot_response",
        "feedback": "Proyecto iniciado. Ya creaste una respuesta basica para tu bot.",
    },
]


GLOSSARY_TERMS = [
    {
        "term": "Algoritmo",
        "definition": "Conjunto ordenado de pasos que permite resolver un problema.",
        "example": "Calcular un promedio: leer notas, sumarlas, dividir por la cantidad y mostrar el resultado.",
    },
    {
        "term": "Variable",
        "definition": "Espacio con nombre donde se guarda un dato que puede cambiar durante la ejecucion.",
        "example": 'nombre = "Sandra"',
    },
    {
        "term": "Constante",
        "definition": "Valor que se considera fijo dentro del programa.",
        "example": "IVA = 0.21",
    },
    {
        "term": "Dato",
        "definition": "Valor o informacion que usa un programa para procesar una tarea.",
        "example": "Una edad, un precio, una ciudad o una respuesta del usuario.",
    },
    {
        "term": "Bucle",
        "definition": "Grupo de instrucciones que se repiten mientras se cumpla una condicion o durante una cantidad de veces.",
        "example": "for numero in range(1, 6):",
    },
    {
        "term": "Estructura selectiva",
        "definition": "Bloque que permite tomar decisiones logicas dentro de un programa.",
        "example": "if edad >= 18:",
    },
    {
        "term": "Estructura repetitiva",
        "definition": "Bloque que permite ejecutar instrucciones varias veces.",
        "example": "while contador <= 5:",
    },
    {
        "term": "Pseudocodigo",
        "definition": "Forma de escribir la logica de un algoritmo con lenguaje simple antes de programarlo.",
        "example": "Leer precio, calcular total, escribir total.",
    },
    {
        "term": "Diagrama de flujo",
        "definition": "Representacion visual de un algoritmo usando simbolos y flechas.",
        "example": "Inicio -> Leer edad -> Decision -> Mostrar resultado.",
    },
    {
        "term": "Identificador",
        "definition": "Nombre que se usa para reconocer variables, funciones u otros elementos del programa.",
        "example": "total_ventas",
    },
    {
        "term": "Funcion",
        "definition": "Bloque reutilizable de codigo que puede recibir datos y devolver un resultado.",
        "example": "def saludar(nombre):",
    },
    {
        "term": "Vector",
        "definition": "Estructura que almacena varios valores en una sola dimension.",
        "example": "ventas = [1200, 1500, 1800]",
    },
    {
        "term": "Matriz",
        "definition": "Estructura que organiza datos en filas y columnas.",
        "example": "matriz = [[1, 2], [3, 4]]",
    },
    {
        "term": "Python",
        "definition": "Lenguaje de programacion interpretado, claro y usado en datos, automatizacion, web e IA.",
        "example": 'print("Hola Python")',
    },
    {
        "term": "Programa",
        "definition": "Conjunto de instrucciones escritas en un lenguaje de programacion para realizar una tarea.",
        "example": "Un archivo app.py con variables, condiciones y salidas.",
    },
    {
        "term": "VS Code",
        "definition": "Editor de codigo usado para escribir, ejecutar y organizar proyectos de programacion.",
        "example": "Abrir carpeta -> crear app.py -> ejecutar en terminal.",
    },
]


LESSON_GLOSSARY = {
    0: ["Variable", "Dato", "Identificador"],
    1: ["Variable", "Python", "VS Code"],
    2: ["Dato", "Estructura selectiva", "Python"],
    3: ["Estructura selectiva", "Dato", "Algoritmo"],
    4: ["Variable", "Dato", "Python"],
    5: ["Programa", "Variable", "Python"],
}


def get_lesson(index):
    return LESSONS[index % len(LESSONS)]


def total_lessons():
    return len(LESSONS)


def get_glossary_terms(index):
    names = LESSON_GLOSSARY.get(index, ["Algoritmo", "Variable", "Python"])
    terms_by_name = {item["term"]: item for item in GLOSSARY_TERMS}
    return [terms_by_name[name] for name in names if name in terms_by_name]


def expected_answer(lesson):
    return lesson["starter"]


def normalize_code(code):
    return re.sub(r"\s+", "", code.strip().lower())


def validate_answer(lesson, answer):
    normalized = normalize_code(answer)

    if lesson["validator"] == "favorite_language":
        return "favorite_language=" in normalized and "python" in normalized

    if lesson["validator"] == "print_home_city":
        return normalized in {"print(home_city)", "print( home_city )"}

    if lesson["validator"] == "is_learning":
        return "is_learning=true" in normalized

    if lesson["validator"] == "edad_compare":
        return "edad>=18" in normalized or "18<=edad" in normalized

    if lesson["validator"] == "f_string":
        return normalized.startswith('f"') and "{nombre}" in normalized

    if lesson["validator"] == "bot_response":
        return "bot_response=" in normalized and ("hola" in normalized or "bot" in normalized)

    return normalized == normalize_code(expected_answer(lesson))
