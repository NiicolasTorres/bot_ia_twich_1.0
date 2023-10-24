import random
import numpy as np
import spacy
import json
import irc3
from keras.models import load_model
from irc3 import IrcBot
from data_processing import load_data, preprocess_data

# Cargar el modelo de procesamiento de lenguaje natural de spaCy
nlp = spacy.load("es_core_news_sm")

def load_chatbot_model(model_filename):
    # Carga el modelo del chatbot a partir del archivo proporcionado.
    return load_model(model_filename)

def clean_up_sentence(sentence, nlp):
    # Limpia una oración, tokenizándola y lematizándola.
    doc = nlp(sentence)
    sentence_words = [token.lemma_ for token in doc if not token.is_punct]
    return sentence_words

def bag_of_words(sentence, words):
    # Convierte una oración en un vector binario de palabras.
    sentence_words = clean_up_sentence(sentence, nlp)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence, model, words, classes):
    # Predice la clase de la oración utilizando el modelo del chatbot.
    bow = bag_of_words(sentence, words)
    res = model.predict(np.array([bow]))[0]
    max_index = np.argmax(res)
    category = classes[max_index]
    return category

def get_response(tag, intents):
    # Obtiene una respuesta aleatoria de las intenciones basada en la etiqueta (tag).
    list_of_intents = intents['intents']
    for intent in list_of_intents:
        if intent["tag"] == tag:
            return random.choice(intent['responses'])
    return "Lo siento, no puedo responder a eso."

class ChatBot(IrcBot):
    def __init__(self, channel, nickname, server, port, model_filename, intents_filename):
        super().__init__()
        self.channel = channel
        self.words = []
        self.classes = []
        self.model = load_chatbot_model(model_filename)
        self.intents = load_data(intents_filename)

        if self.intents:
            self.training, self.words, self.classes = preprocess_data(self.intents)

    @classmethod
    def reload(cls, module, target, k):
        # Maneja la recarga de módulos si es necesario
        pass

    def on_ready(self, **kwargs):
        self.join(self.channel)

    @irc3.event(irc3.rfc.PRIVMSG)
    def on_privmsg(self, event, mask, target, data, **kwargs):
        message = data['message']
        if message.startswith('!exit'):
            self.die()
        else:
            self.respond_to_message(message)

    def predict_intent(self, message):
        return predict_class(message, self.model, self.words, self.classes)

    def get_response(self, intent):
        return get_response(intent, self.intents)

    def respond_to_message(self, message):
        intent = self.predict_intent(message)

        if intent == 'buscar_en_google' or intent == 'buscar_que_es_un_triangulo':
            # Realiza la búsqueda en Google y obtén los resultados
            query = message  # Usar el mensaje del usuario como consulta de búsqueda
            search_results = search_google(query)

            if search_results:
                response = "Encontré algunos resultados en Google:\n"
                response += "\n".join(search_results)
            else:
                response = "Lo siento, no pude encontrar resultados en Google para tu consulta."
        else:
            # Si no es una búsqueda en Google, obtener una respuesta de las intenciones definidas
            response = self.get_response(intent)

        # Enviar la respuesta al chat de Twitch
        self.privmsg(self.channel, response)

def search_google(query):
    # Realiza una búsqueda en Google y devuelve los primeros resultados como una lista de cadenas
    search_results = []
    # Aquí deberías realizar la búsqueda en Google y obtener los resultados
    # Puedes usar la función que ya tienes para buscar en Google
    return search_results


