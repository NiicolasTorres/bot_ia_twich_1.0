import random
import json
import pickle
import numpy as np
import spacy
from nltk.stem import WordNetLemmatizer

# Para crear la red neuronal
from keras.models import Sequential
from keras.metrics import Accuracy
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

nlp = spacy.load("es_core_news_sm")

intents = json.loads(open('intents.json').read())

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '¿', '.', ',']

# Clasifica los patrones y las categorías
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

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Pasa la información a unos y ceros según las palabras presentes en cada categoría para hacer el entrenamiento
training = []
output_empty = [0] * len(classes)
max_words = len(words)

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
print(training)

train_x = [entry[0] for entry in training]
train_y = [entry[1] for entry in training]

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),),activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]),activation='softmax'))

sgd = SGD(learning_rate=0.001, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=[Accuracy()])
train_process = model.fit(np.array(train_x),np.array(train_y),epochs=100,batch_size=5,verbose=1)
model.save('chatbot_model.keras')


                        
            
            

