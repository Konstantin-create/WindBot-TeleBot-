# Imports
import os
import telebot

import modules.get_weather as get_weather
import modules.make_png_from_table as make_png_from_table

with open("token", "r") as file:
    TOKEN = file.read()
    file.close()

# Variables
language_select = {id: {}}

# Bot indication
bot = telebot.TeleBot(token=TOKEN)

# Markups
# Language markup
language_keyboard = telebot.types.ReplyKeyboardMarkup()
buttons = ["Русский", "English"]
language_keyboard.add(*buttons)

# Generate png to Results
generate_png_inline_markup = telebot.types.InlineKeyboardMarkup()


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
        language_select[message.from_user.id] = dict([('lang', 'ru')])
    elif message.text == "English":
        bot.send_message(message.chat.id, "Excellent! English has been chosen!",
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        language_select[message.from_user.id] = dict([('lang', 'en')])
    else:
        try:
            try:
                if language_select[message.from_user.id]["lang"] == "ru":
                    bot.send_message(message.chat.id, "⏳Пожалуйста, подождите 3 секунды, ваш запрос обрабатывается⏳")
                    generate_png_inline_markup.add(telebot.types.InlineKeyboardButton(
                        "Таблица отображается криво! Отправить PNG фотографией!", callback_data='send_png'))
                elif language_select[message.from_user.id]["lang"] == "en":
                    bot.send_message(message.chat.id, "⏳Please, wait for 3 seconds, your request is being processed⏳")
                    generate_png_inline_markup.add(telebot.types.InlineKeyboardButton(
                        "The table is not displayed beautifully! Send data as PNG photo!", callback_data='send_png'))
            except:
                bot.send_message(message.chat.id, "Please, choose language for your profile! You can do it in /start\n"
                                                  "Пожалуйста выберете язык для вашего профиля! "
                                                  "Вы можете сделать это в меню /start")
                return
            data = message.text
            if data.isalpha():
                wind_table = str(get_weather.get_weather_from_city(data, 1))
                with open(f"img//{message.chat.id}.txt", "w") as user_cash_file:
                    user_cash_file.write(wind_table)
                    user_cash_file.close()
                msg = bot.send_message(message.chat.id,
                                       "Recourse: windy.com\n" + "<pre>" + wind_table + "</pre>",
                                       parse_mode="HTML", reply_markup=generate_png_inline_markup)
            else:
                try:
                    x, y = data.split(",")
                    wind_table = str(get_weather.get_weather_from_coords(x, y, 1))
                    with open(f"img//{message.chat.id}.txt", "w") as user_cash_file:
                        user_cash_file.write(wind_table)
                        user_cash_file.close()
                    msg = bot.send_message(message.chat.id,
                                           "Recourse: windy.com" + "<pre>" + wind_table + "</pre>",
                                           parse_mode="HTML", reply_markup=generate_png_inline_markup)
                except:
                    try:
                        if language_select[message.from_user.id]["lang"] == "ru":
                            bot.send_message(message.chat.id,
                                             "Неверный формат координат!")
                        elif language_select[message.from_user.id]["lang"] == "en":
                            bot.send_message(message.chat.id,
                                             "Wrong format of geographic coords!")
                    except:
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


@bot.callback_query_handler(func=lambda message: True)
def send_png(message):
    with open(f"img/{str(message.from_user.id)}.txt", "r") as user_cash_file:
        table_data = user_cash_file.read()
        user_cash_file.close()
    make_png_from_table.make_png(table_data, message.from_user.id)
    with open(f"img/{str(message.from_user.id)}.png", "rb") as f:
        bot.send_photo(message.from_user.id, f, reply_markup=telebot.types.ReplyKeyboardRemove())
        f.close()
    os.remove(f"img/{message.from_user.id}.txt")
    os.remove(f"img/{message.from_user.id}.png")


# Non stop polling
bot.infinity_polling()
