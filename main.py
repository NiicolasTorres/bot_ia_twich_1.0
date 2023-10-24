import irc3
from irc3 import IrcBot
from irc3.plugins.command import command
from chatbot import ChatBot

@irc3.plugin
class MyPlugin:

    def __init__(self, bot):
        self.bot = bot

    # Evento para manejar la conexión
    @irc3.event(irc3.rfc.CONNECTED)
    def on_connected(self, **kwargs):
        self.bot.join('#rolcrowley')

    # Comando para manejar mensajes
    @command
    def mensaje(self, mask, target, args):
        # Reemplaza este ejemplo con tu lógica de procesamiento de mensajes
        self.bot.privmsg(target, f'Recibido: {args}')

def run_bot(config):
    return IrcBot.from_config(config)

if __name__ == '__main__':
    # Configura y ejecuta el bot
    config = {
        'nick': 'xxxxxxxxxxxx',  # Nombre de usuario de tu bot
        'host': 'irc.twitch.tv',  # Servidor de Twitch
        'port': 6667,  # Puerto de Twitch
        'channels': ['#xxxxxxxx'],  # Canales a los que se unirá el bot
        'password': 'xxxxxxxxxxxxxxxxx'  # Token de autenticación de tu bot
    }
    bot = run_bot(config)
    chatbot = ChatBot(channel=config['channels'][0], nickname=config['nick'], server=config['host'], port=config['port'], model_filename='chatbot_model.keras', intents_filename='intents.json')
    bot.run(forever=True)

