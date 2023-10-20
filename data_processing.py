import json
import pickle
import spacy
import random

# Cargar el modelo de procesamiento de lenguaje natural de spaCy
nlp = spacy.load("es_core_news_sm")

def load_data(filename):
    #Carga los datos de intenciones (intents) desde un archivo JSON
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


def preprocess_data(intents):
    #Realiza el preprocesamiento de datos de intenciones para entrenar el chatbot
    words = []
    classes = []
    documents = []
    ignore_letters = ['?', '!', '¿', '.', ',']

    # Iterar a través de las intenciones y patrones en los datos
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            doc = nlp(pattern)
            word_list = [token.lemma_ for token in doc if not token.is_punct]
            words.extend(word_list)
            documents.append((word_list, intent["tag"]))
            if intent["tag"] not in classes:
                classes.append(intent["tag"])

    words = [word for word in words if word not in ignore_letters]
    words = sorted(set(words))

    # Guardar las palabras y clases procesadas en archivos pickle
    pickle.dump(words, open('words.pkl', 'wb'))
    pickle.dump(classes, open('classes.pkl', 'wb'))

    training = []
    output_empty = [0] * len(classes)
    max_words = len(words)

    # Crear datos de entrenamiento en formato de entrada/salida
    for document in documents:
        bag = [0] * max_words
        word_patterns = document[0]
        word_patterns = [word.lower() for word in word_patterns]
        for word in word_patterns:
            if word in words:
                bag[words.index(word)] = 1
        output_row = list(output_empty)
        output_row[classes.index(document[1])] = 1
        training.append([bag, output_row])

    random.shuffle(training)

    return training, words, classes
