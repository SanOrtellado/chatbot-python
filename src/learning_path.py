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


def get_lesson(index):
    return LESSONS[index % len(LESSONS)]


def total_lessons():
    return len(LESSONS)


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
