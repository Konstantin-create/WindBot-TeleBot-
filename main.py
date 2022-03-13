# Imports
import telebot

import modules.get_weather as get_weather

with open("token", "r") as file:
    TOKEN = file.read()
    file.close()

# Variables
language_select = {}

# Bot indication
bot = telebot.TeleBot(token=TOKEN)

# Markups
language_keyboard = telebot.types.ReplyKeyboardMarkup()
buttons = ["Русский", "Английский"]
language_keyboard.add(*buttons)


# Message handlers
@bot.message_handler(commands=['start'])
def start_cm(message):
    bot.send_message(message.chat.id,
                     "Hey! Choose your preferred language\n"
                     "Привет! Выбери предпочтительный язык", reply_markup=language_keyboard)


@bot.message_handler(content_types=["text"])
def place_input(message):
    if message.text == "Русский":
        bot.send_message(message.chat.id, "Отлично! Выбран русский язык!",
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        language_select[message.from_user.id]["lang"] = "ru"
    elif message.text == "English":
        bot.send_message(message.chat.id, "Excellent! English has been chosen!",
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        language_select[message.from_user.id]["lang"] = "en"
    else:
        try:
            if language_select[message.from_user.id]["lang"] == "ru":
                bot.send_message(message.chat.id, "⏳Пожалуйста, подождите 3 секунды, ваш запрос обрабатывается⏳")
            elif language_select[message.from_user.id]["lang"] == "en":
                bot.send_message(message.chat.id, "⏳Please, wait for 3 seconds, your request is being processed⏳")
            else:
                bot.send_message(message.chat.id, "Please, choose language for your profile! You can do it in /start\n"
                                                  "Пожалуйста выберете язык для вашего профиля! "
                                                  "Вы можете сделать это в меню /start")
            data = message.text
            if data.isalpha():
                bot.send_message(message.chat.id,
                                 "Recourse: windy.com\n" + "<pre>" + str(get_weather.get_weather_from_city(data, 1)) + "</pre>",
                                 parse_mode="HTML")
            else:
                try:
                    x, y = data.split(",")
                    bot.send_message(message.chat.id,
                                     "Recourse: windy.com"+"<pre>" + str(get_weather.get_weather_from_coords(x, y, 1)) + "</pre>",
                                     parse_mode="HTML")
                except:
                    if language_select[message.from_user.id]["lang"] == "ru":
                        bot.send_message(message.chat.id,
                                         "Неверный формат координат!")
                    elif language_select[message.from_user.id]["lang"] == "en":
                        bot.send_message(message.chat.id,
                                         "Wrong format of geographic coords!")
                    else:
                        bot.send_message(message.chat.id,
                                         "Please, choose language for your profile! You can do it in /start\n"
                                         "Пожалуйста выберете язык для вашего профиля! "
                                         "Вы можете сделать это в меню /start")
        except Exception as e:
            if language_select[message.from_user.id]["lang"] == "ru":
                bot.send_message(message.chat.id,
                                 f"Ошибка: {e}. Попробуйте в следующий раз")
            elif language_select[message.from_user.id]["lang"] == "en":
                bot.send_message(message.chat.id,
                                 f"Error: {e}. Try next time")
            else:
                bot.send_message(message.chat.id,
                                 "Please, choose language for your profile! You can do it in /start\n"
                                 "Пожалуйста выберете язык для вашего профиля! "
                                 "Вы можете сделать это в меню /start")


# Non stop polling
bot.infinity_polling()
