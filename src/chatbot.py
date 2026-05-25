import json
import pickle
import random
from pathlib import Path

import numpy as np
from tensorflow.keras.models import load_model

from nlp_utils import bag_of_words, ensure_nltk_data


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "intents.json"
MODEL_DIR = BASE_DIR / "model"
ERROR_THRESHOLD = 0.25
EXIT_WORDS = {"salir", "chau", "adios", "terminar"}


def load_resources():
    ensure_nltk_data()

    with DATA_PATH.open("r", encoding="utf-8") as file:
        intents = json.load(file)

    with (MODEL_DIR / "words.pkl").open("rb") as file:
        words = pickle.load(file)

    with (MODEL_DIR / "classes.pkl").open("rb") as file:
        classes = pickle.load(file)

    model = load_model(MODEL_DIR / "chatbot_model.keras")
    return intents, words, classes, model


def predict_class(sentence, model, words, classes):
    bow = bag_of_words(sentence, words)
    probabilities = model.predict(np.array([bow]), verbose=0)[0]

    results = [
        {"intent": classes[index], "probability": float(probability)}
        for index, probability in enumerate(probabilities)
        if probability > ERROR_THRESHOLD
    ]
    results.sort(key=lambda item: item["probability"], reverse=True)
    return results


def get_response(predicted_intents, intents_json):
    if not predicted_intents:
        return "No estoy seguro de haber entendido. Podrias escribirlo de otra forma?"

    tag = predicted_intents[0]["intent"]
    for intent in intents_json["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])

    return "No encontre una respuesta para esa intencion."


def main():
    if not (MODEL_DIR / "chatbot_model.keras").exists():
        print("Primero entrena el modelo con: python src/train.py")
        return

    intents, words, classes, model = load_resources()

    print("Chatbot iniciado. Escribi 'salir' para terminar.")
    while True:
        message = input("Vos: ").strip()

        if not message:
            continue

        if message.lower() in EXIT_WORDS:
            print("Bot: Hasta luego.")
            break

        predicted = predict_class(message, model, words, classes)
        response = get_response(predicted, intents)
        print(f"Bot: {response}")


if __name__ == "__main__":
    main()
