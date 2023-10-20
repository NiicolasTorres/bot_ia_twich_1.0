from data_processing import load_data, preprocess_data
from keras.models import Sequential
from keras.layers import Dense
import numpy as np

# Cargar datos e intenciones
intents = load_data('intents.json')
print("Contenido de intents:")
print(intents)
if intents is not None:
    training, words, classes = preprocess_data(intents)
else:
    print("Error: No se pudo cargar el archivo intents.json")

# Crear el modelo
model = Sequential()
model.add(Dense(128, input_shape=(len(words),), activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(len(classes), activation='softmax'))

# Compilar y entrenar el modelo
X = np.array([item[0] for item in training])
y = np.array([item[1] for item in training])
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, y, epochs=200, batch_size=5, verbose=1)

# Guardar el modelo
model.save('chatbot_model.keras')