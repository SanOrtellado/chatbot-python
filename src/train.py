import json
import pickle
import random
from pathlib import Path

import numpy as np
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import SGD

from nlp_utils import ensure_nltk_data, normalize_words, tokenize


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "intents.json"
MODEL_DIR = BASE_DIR / "model"
IGNORE_WORDS = {"?", "!", ".", ",", ";", ":"}


def load_intents():
    with DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def build_training_data(intents):
    words = []
    classes = []
    documents = []

    for intent in intents["intents"]:
        tag = intent["tag"]
        classes.append(tag)

        for pattern in intent["patterns"]:
            tokens = tokenize(pattern)
            words.extend(tokens)
            documents.append((tokens, tag))

    vocabulary = sorted(set(normalize_words(words, IGNORE_WORDS)))
    classes = sorted(set(classes))

    training = []
    output_empty = [0] * len(classes)

    for tokens, tag in documents:
        pattern_words = normalize_words(tokens, IGNORE_WORDS)
        bag = [1 if word in pattern_words else 0 for word in vocabulary]

        output_row = output_empty.copy()
        output_row[classes.index(tag)] = 1
        training.append([bag, output_row])

    random.shuffle(training)
    train_x = np.array([row[0] for row in training], dtype=np.float32)
    train_y = np.array([row[1] for row in training], dtype=np.float32)

    return vocabulary, classes, train_x, train_y


def create_model(input_size, output_size):
    model = Sequential(
        [
            Dense(128, input_shape=(input_size,), activation="relu"),
            Dropout(0.5),
            Dense(64, activation="relu"),
            Dropout(0.5),
            Dense(output_size, activation="softmax"),
        ]
    )

    optimizer = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
    model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"])
    return model


def main():
    ensure_nltk_data()
    MODEL_DIR.mkdir(exist_ok=True)

    intents = load_intents()
    vocabulary, classes, train_x, train_y = build_training_data(intents)

    with (MODEL_DIR / "words.pkl").open("wb") as file:
        pickle.dump(vocabulary, file)

    with (MODEL_DIR / "classes.pkl").open("wb") as file:
        pickle.dump(classes, file)

    model = create_model(len(vocabulary), len(classes))
    model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)
    model.save(MODEL_DIR / "chatbot_model.keras")

    print("Entrenamiento completado.")
    print(f"Intenciones: {len(classes)}")
    print(f"Vocabulario: {len(vocabulary)} palabras")
    print(f"Modelo guardado en: {MODEL_DIR}")


if __name__ == "__main__":
    main()
