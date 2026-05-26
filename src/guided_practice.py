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
    {
        "topic": "Operadores aritmeticos",
        "question": "Que operador se usa para obtener el resto de una division?",
        "options": ["%", "/", "**"],
        "answer": 0,
        "feedback_ok": "Correcto. `%` devuelve el resto de una division.",
        "feedback_bad": "`/` divide y `**` calcula potencia. Para el resto se usa `%`.",
        "mini_lesson": "Ejemplo: `10 % 3` devuelve `1`.",
    },
    {
        "topic": "Operadores relacionales",
        "question": "Que devuelve una comparacion como `edad >= 18`?",
        "options": ["True o False", "Una lista", "Un texto obligatorio"],
        "answer": 0,
        "feedback_ok": "Correcto. Las comparaciones devuelven valores booleanos.",
        "feedback_bad": "Una comparacion evalua una condicion y devuelve `True` o `False`.",
        "mini_lesson": "Ejemplo: `20 >= 18` devuelve `True`.",
    },
    {
        "topic": "Operadores logicos",
        "question": "Que operador exige que dos condiciones sean verdaderas?",
        "options": ["and", "or", "not"],
        "answer": 0,
        "feedback_ok": "Correcto. `and` requiere que ambas condiciones se cumplan.",
        "feedback_bad": "`or` acepta una condicion verdadera y `not` invierte el resultado. Para ambas, usa `and`.",
        "mini_lesson": "Ejemplo: `edad >= 18 and saldo > 0`.",
    },
    {
        "topic": "While",
        "question": "Cuando conviene usar un bucle while?",
        "options": [
            "Cuando quiero repetir mientras una condicion sea verdadera.",
            "Cuando quiero mostrar un texto una sola vez.",
            "Cuando quiero crear una variable de texto.",
        ],
        "answer": 0,
        "feedback_ok": "Correcto. `while` repite mientras la condicion sea verdadera.",
        "feedback_bad": "`while` no es para mostrar una sola vez ni para crear variables: es para repetir con condicion.",
        "mini_lesson": "Ejemplo: `while contador <= 5:`.",
    },
    {
        "topic": "Vectores",
        "question": "Como representamos normalmente un vector en Python?",
        "options": ["Con una lista", "Con un print", "Con un if"],
        "answer": 0,
        "feedback_ok": "Correcto. En Python un vector puede representarse con una lista.",
        "feedback_bad": "`print` muestra y `if` decide. Para varios valores en una dimension, usa una lista.",
        "mini_lesson": "Ejemplo: `ventas = [1200, 1500, 1800]`.",
    },
    {
        "topic": "Matrices",
        "question": "Como se puede representar una matriz en Python?",
        "options": ["Como una lista de listas", "Como una sola cadena", "Solo con input"],
        "answer": 0,
        "feedback_ok": "Correcto. Una matriz puede ser una lista que contiene otras listas.",
        "feedback_bad": "Una cadena guarda texto e `input` lee datos. Una matriz se puede representar como lista de listas.",
        "mini_lesson": "Ejemplo: `matriz = [[1, 2], [3, 4]]`.",
    },
]


def get_question(index):
    return QUESTIONS[index]


def total_questions():
    return len(QUESTIONS)


def is_complete(index):
    return index >= total_questions()
