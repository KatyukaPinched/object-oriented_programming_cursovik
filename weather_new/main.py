from WeatherBot import WeatherBot

if __name__ == "__main__":
    token = open('token.txt','r')
    weather_bot = WeatherBot(*token)
    weather_bot.bot.polling(none_stop=True)
    token.close()