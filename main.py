import chatbot

if __name__ == "__main__":
    # Cargar las intenciones y realizar el preprocesamiento de datos
    intents = chatbot.load_data('intents.json')
    training, words, classes = chatbot.preprocess_data(intents)
    # Cargar el modelo del chatbot
    model = chatbot.load_chatbot_model('chatbot_model.keras')

    # Bucle principal para la conversación con el usuario
    while True:
        message = input("Tú: ")
        if message.lower() == 'exit':
            break
        # Predecir la intención del mensaje y obtener una respuesta
        intent = chatbot.predict_class(message, model, words, classes)
        response = chatbot.get_response(intent, intents)
        print(f"Bot: {response}")