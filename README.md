# Chatbot con Python, NLTK y Keras

Proyecto de chatbot educativo que usa procesamiento de lenguaje natural y una red neuronal simple para clasificar mensajes de usuario en intenciones y responder con frases relevantes.

El objetivo es aprender el flujo basico de un chatbot basado en machine learning: preparar texto, convertirlo en datos numericos, entrenar un modelo y usarlo en una conversacion por consola o desde una interfaz web.

## Que hace

- Lee un dataset de intenciones desde `data/intents.json`.
- Limpia y tokeniza frases con NLTK.
- Entrena una red neuronal con Keras/TensorFlow.
- Guarda el modelo entrenado y los archivos auxiliares.
- Permite conversar con el bot desde la terminal.
- Incluye una interfaz web con Streamlit para mostrar la interaccion del usuario.

## Stack

- Python
- NLTK
- TensorFlow / Keras
- NumPy
- Streamlit

## Version recomendada de Python

Se recomienda usar Python 3.10, 3.11 o 3.12 para evitar problemas de compatibilidad con TensorFlow.

## Estructura

```text
chatbot-python/
|-- app.py
|-- assets/
|   `-- linkedin_post.md
|-- data/
|   `-- intents.json
|-- src/
|   |-- chatbot.py
|   |-- nlp_utils.py
|   `-- train.py
|-- .gitignore
|-- README.md
`-- requirements.txt
```

## Como ejecutar

1. Entrar a la carpeta del proyecto:

```bash
cd chatbot-python
```

2. Crear y activar un entorno virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

Este archivo instala las dependencias necesarias para abrir la interfaz web en modo demo.

Si queres usar la red neuronal entrenada con TensorFlow, instala tambien las dependencias de machine learning usando Python 3.10, 3.11 o 3.12:

```bash
pip install -r requirements-ml.txt
```

4. Entrenar el modelo:

```bash
python src/train.py
```

5. Iniciar el chatbot por consola:

```bash
python src/chatbot.py
```

Para salir de la conversacion, escribi `salir`, `chau` o `adios`.

6. Iniciar la interfaz web:

```bash
streamlit run app.py
```

La interfaz puede abrir en modo demo aunque TensorFlow no este instalado. Para usar el modelo de red neuronal, usa Python 3.10, 3.11 o 3.12, instala `requirements-ml.txt` y ejecuta `python src/train.py`.

## Como funciona

El archivo `data/intents.json` contiene categorias de mensajes llamadas intenciones. Cada intencion tiene ejemplos de frases del usuario y posibles respuestas.

Durante el entrenamiento, el proyecto:

1. Tokeniza las frases.
2. Normaliza las palabras con stemming para reducir variaciones.
3. Crea una bolsa de palabras para representar cada frase.
4. Entrena una red neuronal que aprende a clasificar la intencion.
5. Guarda el modelo en `model/chatbot_model.keras`.

Cuando el usuario escribe un mensaje, el chatbot transforma ese texto con el mismo proceso y predice la intencion mas probable.

## Ideas de mejora

- Agregar mas intenciones y ejemplos de entrenamiento.
- Mejorar el diseno de la interfaz web.
- Guardar el historial de conversacion.
- Conectar el bot con Telegram, WhatsApp o Discord.
- Medir precision y matriz de confusion del modelo.

## Aprendizajes

Este proyecto practica conceptos clave de NLP y deep learning de forma accesible:

- Limpieza y preparacion de texto.
- Representacion numerica de palabras.
- Clasificacion multiclase.
- Entrenamiento y uso de modelos.
- Construccion de interfaces conversacionales.
