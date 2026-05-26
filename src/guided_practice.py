QUESTIONS = [
    {
        "topic": "Variables",
        "question": "Para que utilizan las variables los programas?",
        "options": [
            "Para almacenar informacion para su uso posterior.",
            "Para mostrar informacion en pantalla.",
            "Para cambiar el color de la terminal.",
        ],
        "answer": 0,
        "feedback_ok": "Correcto. Una variable guarda datos para usarlos despues.",
        "feedback_bad": "Casi. Mostrar informacion se hace con `print`. Las variables guardan datos.",
        "mini_lesson": "Ejemplo: `nombre = \"Sandra\"` guarda el texto Sandra en la variable `nombre`.",
    },
    {
        "topic": "Salida",
        "question": "Que instruccion se usa para mostrar informacion en pantalla?",
        "options": ["input()", "print()", "while"],
        "answer": 1,
        "feedback_ok": "Correcto. `print()` muestra informacion en pantalla.",
        "feedback_bad": "`input()` lee datos y `while` repite instrucciones. Para mostrar se usa `print()`.",
        "mini_lesson": "Ejemplo: `print(\"Hola Python\")` muestra un mensaje.",
    },
    {
        "topic": "Entrada",
        "question": "Que hace la funcion input() en Python?",
        "options": [
            "Recibe informacion escrita por el usuario.",
            "Suma dos numeros automaticamente.",
            "Crea un bucle.",
        ],
        "answer": 0,
        "feedback_ok": "Correcto. `input()` permite recibir datos del usuario.",
        "feedback_bad": "`input()` no calcula ni repite: sirve para leer informacion ingresada por el usuario.",
        "mini_lesson": "Ejemplo: `nombre = input(\"Nombre: \")` guarda lo que escribe el usuario.",
    },
    {
        "topic": "Condicionales",
        "question": "Para que sirve una estructura if?",
        "options": [
            "Para tomar decisiones segun una condicion.",
            "Para guardar muchos datos.",
            "Para instalar Python.",
        ],
        "answer": 0,
        "feedback_ok": "Correcto. `if` permite ejecutar codigo solo si se cumple una condicion.",
        "feedback_bad": "`if` no guarda datos ni instala herramientas. Sirve para tomar decisiones.",
        "mini_lesson": "Ejemplo: `if edad >= 18:` evalua si una persona es mayor de edad.",
    },
    {
        "topic": "Bucles",
        "question": "Que estructura usarias para repetir instrucciones una cantidad conocida de veces?",
        "options": ["for", "if", "print"],
        "answer": 0,
        "feedback_ok": "Correcto. `for` es ideal para repetir o recorrer secuencias.",
        "feedback_bad": "`if` decide y `print` muestra. Para repetir una cantidad conocida, usa `for`.",
        "mini_lesson": "Ejemplo: `for numero in range(1, 6): print(numero)`.",
    },
    {
        "topic": "Listas",
        "question": "Que estructura permite guardar varios valores en una sola variable?",
        "options": ["Una lista", "Un comentario", "Un operador relacional"],
        "answer": 0,
        "feedback_ok": "Correcto. Una lista guarda varios elementos.",
        "feedback_bad": "Los comentarios documentan codigo y los operadores comparan. Para varios valores, usa una lista.",
        "mini_lesson": "Ejemplo: `productos = [\"notebook\", \"mouse\", \"teclado\"]`.",
    },
]


def get_question(index):
    return QUESTIONS[index % len(QUESTIONS)]


def total_questions():
    return len(QUESTIONS)
