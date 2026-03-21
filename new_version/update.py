
from functions_update_v2 import *
from message_text import *

# Указываем токен (не забудьте заменить на ваш токен)
  # Замените на ваш токен
keyboard_massive = []
final_text = ''
new_text = ''

"""
import requests
from requests.adapters import HTTPAdapter

session = requests.Session()

# 1. Сначала настраиваем адаптер
adapter = HTTPAdapter(pool_connections=50, pool_maxsize=50)
session.mount('https://', adapter)

# 2. Делаем тестовый запрос (пул создается при первом обращении)
try:
    session.get('https://api.telegram.org', timeout=1)
except:
    pass

# 3. Теперь получаем АКТУАЛЬНЫЙ пул
actual_adapter = session.get_adapter('https://api.telegram.org')
pool = actual_adapter.poolmanager.connection_from_url('https://api.telegram.org')

print(f"Хост: {pool.host}")
print(f"Макс. соединений в пуле: {pool.pool.maxsize}") # Должно стать 20
print(f"Свободных слотов сейчас: {pool.pool.qsize()}")


Теперь запросы через session.get(...) будут использовать расширенный пул



# from telebot import apihelper
#
# # Пример настройки прокси
# apihelper.proxy = {'https': 'http://185.250.249.154:1080'}
"""


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global final_text
    global keyboard_massive

    text = message.text
    chat_id = message.from_user.id

    if text == "/start":
        print(message)
        bot.send_message(message.from_user.id, text=f"Приветствую тебя, @{message.from_user.username}!")
        msg = "only start"
        keyboard_massive = [['ТРЕУГОЛЬНИК', 'Triangle'],
                            ['ЧЕТЫРЁХУГОЛЬНИК', 'Geometry'],
                            ['ОКРУЖНОСТЬ И КРУГ', 'Circle'],
                            ['ПРЯМАЯ', 'Straight'],
                            ['УГОЛ', 'Corner']]

        print(message.chat.id)

        list_clear(message)
        message_layer(chat_id, geometry_OPR_text, "Geometry", 'приветствие.jpg', keyboard_massive, msg)

        # inline_keyboard(keyboard_massive, call_chat_id=chat_id, msg=msg, media="приветствие.jpg")

    elif text == "/help":
        bot.send_message(message.from_user.id, "Напиши /start")

    elif text == "/stop_bot":
        i = 0
        for item in ids_list:
            bot.send_message(ids_list[i], text="Увы, я отключаюсь до завтра. Спокойной ночи!")
            i += 1
        bot.stop_polling()
    else:
        print("hhh")
        print(text.lower())
        if text.lower() in assotiations:

            message.text = assotiations[text.lower()]
            choice(message.text, message.from_user.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    bot.answer_callback_query(call.id)

    choice(call.data, call.message.chat.id)
        # Запускаем бота

bot.polling(none_stop=True)