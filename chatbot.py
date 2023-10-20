import random
import numpy as np
import spacy
from data_processing import load_data, preprocess_data
from keras.models import load_model
from googlesearch import search

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

def search_google(query):
    # Realiza una búsqueda en Google y devuelve los primeros resultados como una lista de cadenas
    search_results = []
    for result in search(query, num=5, stop=5, lang="es"):
        search_results.append(result)
    return search_results

if __name__ == "__main__":
    # Cargar datos de intenciones y procesarlo
    intents = load_data('intents.json')
    if intents is not None:
        training, words, classes = preprocess_data(intents)
    else:
        print("Error: No se pudo cargar el archivo intents.json")
    
    # Cargar el modelo del chatbot
    model = load_chatbot_model('chatbot_model.keras')

    # Iniciar el bucle de conversación con el usuario
    while True:
        message = input("Tú: ")
        if message.lower() == 'exit':
            break
        intent = predict_class(message, model, words, classes)

        if intent == 'buscar_en_google' or intent == 'buscar_que_es_un_triangulo':
            # Si la intención es buscar en Google, realizar la búsqueda
            query = message  # Usar el mensaje del usuario como consulta de búsqueda
            search_results = search_google(query)

            if search_results:
                response = "Encontré algunos resultados en Google:\n"
                response += "\n".join(search_results)
            else:
                response = "Lo siento, no pude encontrar resultados en Google para tu consulta."
        else:
            # Si no es una búsqueda en Google, obtener una respuesta de las intenciones definidas
            response = get_response(intent, intents)

        print(f"Bot: {response}")