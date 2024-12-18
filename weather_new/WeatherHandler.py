import requests
import json
from telebot import types

API = '23f9689ab554f3588bec403da4fa41ef'

class WeatherHandler:
    def __init__(self, bot):
        self.bot = bot
        self.weather_data = None

    def handle_message(self, message):
        if message.content_type == 'text':
            self.handle_text_message(message)
        else:
            self.handle_non_text_message(message)

    def handle_non_text_message(self, message):
        if message.content_type == 'audio':
            self.bot.reply_to(message,
                              f"Аудио — бомба!💣🎵 Но данный бот работает только с текстовой информацией, поэтому, пожалуйста, введите запрос корректно))")

        elif message.content_type == 'video_note':
            self.bot.reply_to(message,
                              f"Кружочек — бомба!💣🔴 Но данный бот работает только с текстовой информацией, поэтому, пожалуйста, введите запрос корректно))")

        elif message.content_type == 'voice':
            self.bot.reply_to(message,
                              f"Голосовое — бомба!💣🎙 Но данный бот работает только с текстовой информацией, поэтому, пожалуйста, введите запрос корректно))")

        elif message.content_type == 'video':
            self.bot.reply_to(message,
                              f"Видео — бомба!💣🎥 Но данный бот работает только с текстовой информацией, поэтому, пожалуйста, введите запрос корректно))")

        elif message.content_type == 'photo':
            self.bot.reply_to(message,
                              f"Фото — бомба!💣📸 Но данный бот работает только с текстовой информацией, поэтому, пожалуйста, введите запрос корректно))")
        else: self.bot.reply_to(message,
                          f"Это сообщение не поддерживается. Пожалуйста, введите текстовый запрос.")


    def handle_text_message(self, message):
        city = message.text
        self.weather_data = self.get_weather(city)
        if self.weather_data: self.send_weather_keyboard(message.chat.id)
        else:
            self.bot.reply_to(message, f'Город указан неверно 😡 Не балуйся, пиши нормально 😌')

    def send_weather_keyboard(self, chat_id):
        keyboard = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Температура 🌡", callback_data='temperature')
        btn2 = types.InlineKeyboardButton("Давление 😖", callback_data='pressure')
        keyboard.row(btn1, btn2)
        btn3 = types.InlineKeyboardButton("Облачность 🌫", callback_data='cloud')
        btn4 = types.InlineKeyboardButton("Влажность 💦", callback_data='humidity')
        keyboard.row(btn3, btn4)
        btn5 = types.InlineKeyboardButton("Видимость 🛤", callback_data='visibility')
        btn6 = types.InlineKeyboardButton("Скорость ветра 💨", callback_data='wind')
        keyboard.row(btn5, btn6)
        btn7 = types.InlineKeyboardButton("Ввести новый город 🌇", callback_data='new_city')
        keyboard.row(btn7)

        self.bot.send_message(chat_id, f"Подскажи, какую информацию из предложенной тебе было бы интересно узнать? 🥸",
                              reply_markup=keyboard)

    def get_weather(self, city):
        try:
            res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
            res.raise_for_status()
            return res.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса к API: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Ошибка декодирования JSON: {e}")
            return None

    def handle_callback(self, callback):
        chat_id = callback.message.chat.id
        weather_data = getattr(self, 'weather_data', None)

        if callback.data == 'temperature':
            if -10 > weather_data['main']['temp']:
                self.bot.edit_message_text(
                    f"Температура = {weather_data['main']['temp']} °C 🥶\nОщущается как {weather_data['main']['feels_like']}",
                    chat_id, callback.message.message_id)
            elif weather_data['main']['temp'] > 10:
                self.bot.edit_message_text(
                    f"Температура = {weather_data['main']['temp']} °C 🥵\nОщущается как {weather_data['main']['feels_like']}",
                    chat_id, callback.message.message_id)
            else:
                self.bot.edit_message_text(
                    f"Температура = {weather_data['main']['temp']} °C 😊\nОщущается как {weather_data['main']['feels_like']}",
                    chat_id, callback.message.message_id)
        elif callback.data == 'pressure':
            self.bot.edit_message_text(f"Давление = {weather_data['main']['pressure']} hPa", chat_id,
                                       callback.message.message_id)
        elif callback.data == 'cloud':
            if weather_data['clouds']['all'] <= 20:
                self.bot.edit_message_text(f"Облачность = {weather_data['clouds']['all']}% ☀️", chat_id,
                                           callback.message.message_id)
            elif weather_data['clouds']['all'] <= 40:
                self.bot.edit_message_text(
                    f"Облачность = {weather_data['clouds']['all']}% 🌤", chat_id, callback.message.message_id)
            elif weather_data['clouds']['all'] <= 60:
                self.bot.edit_message_text(
                    f"Облачность = {weather_data['clouds']['all']}% ⛅️", chat_id, callback.message.message_id)
            elif weather_data['clouds']['all'] <= 80:
                self.bot.edit_message_text(
                    f"Облачность = {weather_data['clouds']['all']}% 🌥", chat_id, callback.message.message_id)
            elif weather_data['clouds']['all'] <= 100:
                self.bot.edit_message_text(
                    f"Облачность = {weather_data['clouds']['all']}% ☁️", chat_id, callback.message.message_id)
        elif callback.data == 'humidity':
            if weather_data['main']['humidity'] < 50:
                self.bot.edit_message_text(f"Влажность = {weather_data['main']['humidity']}% ☂️", chat_id,
                                           callback.message.message_id)
            else:
                self.bot.edit_message_text(f"Влажность = {weather_data['main']['humidity']}% ☔️", chat_id,
                                           callback.message.message_id)
        elif callback.data == 'visibility':
            self.bot.edit_message_text(f"Видимость = {weather_data['visibility']} м", chat_id,
                                       callback.message.message_id)
        elif callback.data == 'wind':
            if weather_data['wind']['speed'] < 10:
                self.bot.edit_message_text(f"Скорость ветра = {weather_data['wind']['speed']} м/с 🌬", chat_id,
                                           callback.message.message_id)
            else:
                self.bot.edit_message_text(f"Скорость ветра = {weather_data['wind']['speed']} м/с 🌪", chat_id,
                                           callback.message.message_id)
        elif callback.data == 'new_city':
            self.bot.edit_message_text("Введите новый город:", chat_id, callback.message.message_id)

        if callback.data != 'new_city':
            self.bot.send_message(chat_id, f"Вы хотите еще что-то еще узнать о погоде в данном городе? 🧐")

            keyboard = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("Температура 🌡", callback_data='temperature')
            btn2 = types.InlineKeyboardButton("Давление 😖", callback_data='pressure')
            keyboard.row(btn1, btn2)
            btn3 = types.InlineKeyboardButton("Облачность 🌫", callback_data='cloud')
            btn4 = types.InlineKeyboardButton("Влажность 💦", callback_data='humidity')
            keyboard.row(btn3, btn4)
            btn5 = types.InlineKeyboardButton("Видимость 🛤", callback_data='visibility')
            btn6 = types.InlineKeyboardButton("Скорость ветра 💨", callback_data='wind')
            keyboard.row(btn5, btn6)
            btn7 = types.InlineKeyboardButton("Ввести новый город 🌇", callback_data='new_city')
            keyboard.row(btn7)

            self.bot.send_message(chat_id, "Выберите, что хотите узнать:", reply_markup=keyboard)

    def run(self):
        self.bot.polling()