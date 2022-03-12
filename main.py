import telebot

import modules.get_weather as get_weather

with open("token", "r") as file:
    TOKEN = file.read()
    file.close()

bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def start_cm(message):
    bot.send_message(message.chat.id,
                     "Welcome to WindBot, here you can get weather forecast for any places. "
                     "For use send city name or geographic coordinates. Format: 44.894272, 37.316887")


@bot.message_handler(content_types=["text"])
def place_input(message):
    try:
        bot.send_message(message.chat.id, "⏳Wait for 5 seconds⏳")
        data = message.text
        if data.isalpha():
            bot.send_message(message.chat.id, "<pre>" + str(get_weather.get_weather_from_city(data, 1)) + "</pre>",
                             parse_mode="HTML")
        else:
            try:
                x, y = data.split(",")
                bot.send_message(message.chat.id,
                                 "<pre>" + str(get_weather.get_weather_from_coords(x, y, 1)) + "</pre>",
                                 parse_mode="HTML")
            except Exception as e:
                bot.send_message(message.chat.id, f"Wrong coords. Error: {e}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}. Try next time")


bot.infinity_polling()
