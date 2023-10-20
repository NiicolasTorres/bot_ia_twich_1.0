import random
import json
import pickle
import numpy as np
import spacy

import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

nlp = spacy.load("es_core_news_sm")
intents = json.loads(open('intents.json').read())

with open('words.pkl', 'rb') as words_file:
    words = pickle.load(words_file)
with open('classes.pkl', 'rb') as classes_file:
    classes = pickle.load(classes_file)
    
model = load_model('chatbot_model.keras')

def clean_up_sentence(sentence):
    doc = nlp(sentence)
    sentence_words = [token.lemma_ for token in doc if not token.is_punct]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    max_index = np.where(res ==np.max(res))[0][0]
    category = classes[max_index]
    return category

def get_response(tag, intents_json):
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i["tag"] ==tag:
            result = random.choice(i['responses'])
            break
    return result

while True:
    message=input("")
    ints = predict_class(message)
    res = get_response(ints, intents)
    print(res)