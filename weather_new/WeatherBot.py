from WeatherHandler import WeatherHandler
from telebot import TeleBot, types

class WeatherBot:
    def __init__(self, token):
        self.bot = TeleBot(token)
        self.weather_handler = WeatherHandler(self.bot)
        self.setup_handlers()

    def setup_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.bot.send_message(message.chat.id, f'Здравствуй, {message.from_user.first_name}! '
                                                   f'Введи название города, чтобы получить интересующую тебя информацию о погоде 😇')

        @self.bot.message_handler(content_types=['text', 'photo', 'audio', 'video'])
        def handle_message(message):
            self.weather_handler.handle_message(message)

        @self.bot.callback_query_handler(func=lambda callback: True)
        def callback_message(callback):
            self.weather_handler.handle_callback(callback)