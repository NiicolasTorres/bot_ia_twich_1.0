import random
import json
import pickle
import numpy as np
import spacy
from data_processing import load_data, preprocess_data
from keras.models import load_model

# Cargar el modelo de procesamiento de lenguaje natural de spaCy
nlp = spacy.load("es_core_news_sm")

def load_chatbot_model(model_filename):
    #Carga el modelo del chatbot a partir del archivo proporcionado.
    return load_model(model_filename)

def clean_up_sentence(sentence, nlp):
    #Limpia una oración, tokenizándola y lematizándola.
    doc = nlp(sentence)
    sentence_words = [token.lemma_ for token in doc if not token.is_punct]
    return sentence_words

def bag_of_words(sentence, words):
    #Convierte una oración en un vector binario de palabras.
    sentence_words = clean_up_sentence(sentence, nlp)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence, model, words, classes):
    #Predice la clase de la oración utilizando el modelo del chatbot.
    bow = bag_of_words(sentence, words)
    res = model.predict(np.array([bow]))[0]
    max_index = np.argmax(res)
    category = classes[max_index]
    return category

def get_response(tag, intents):
    #Obtiene una respuesta aleatoria de las intenciones basada en la etiqueta (tag).
    list_of_intents = intents['intents']
    for intent in list_of_intents:
        if intent["tag"] == tag:
            return random.choice(intent['responses'])
    return "Lo siento, no puedo responder a eso."

if __name__ == "__main__":
    # Cargar datos de intenciones y procesarlo
    intents = load_data('intents.json')
    training, words, classes = preprocess_data(intents)
    # Cargar el modelo del chatbot
    model = load_chatbot_model('chatbot_model.keras')

    # Iniciar el bucle de conversación con el usuario
    while True:
        message = input("Tú: ")
        if message.lower() == 'exit':
            break
        intent = predict_class(message, model, words, classes)
        response = get_response(intent, intents)
        print(f"Bot: {response}")