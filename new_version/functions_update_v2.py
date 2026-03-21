from symbol import argument

import telebot
from functions import history_of_acts
from telebot import apihelper

# Пример настройки (нужно найти живой IP и порт)
# Формат: 'socks5://ip:port' или 'http://ip:port'
apihelper.proxy = {'https': 'socks5://HTgMXR:e2cFxC@45.129.184.202:8000'}
# Отключаем проверку сертификатов
# apihelper.CUSTOM_REQUESTER_ARGS = {'verify': False}

# Если вы используете свою сессию (как мы делали раньше),
# то проверку нужно отключить и там:
# response = session.post(url, data=data, files=files, verify=False)



# from update import keyboard_massive
from telebot import types
from telebot.types import InputMediaPhoto
from token_data import *
from message_text import *

from requests.adapters import HTTPAdapter
import requests

# 1. Создаем и настраиваем сессию
session = requests.Session()
adapter = HTTPAdapter(pool_connections=100, pool_maxsize=100) # увеличиваем лимиты
session.mount('https://', adapter)

# 2. Передаем эту сессию в бота
bot = telebot.TeleBot(general_token, threaded=True)
telebot.apihelper.CUSTOM_REQUESTER = session.post # Для POST запросов
# # Или так (в новых версиях):
# bot.threaded = True

keyboard_massive = []
text_to_analyse = []

list_of_history = []
history_id = 0

new_message = True

users_info = {}
arguments = {}
pages = {}



# индексация нужного массива в message_sended
geometry_keys = {"": None,
            "Rectangle": 0,
           "Circle": 1,
           "Circle Ln": 2,
           "Circle Ln H": 3,
           "Circle Ln Ks": 4,
           "Circle OK": 5,
           "Corner": 6,
           "Corner PE": 7,
           "Straight": 8,
           "Triangle": 9,
           "Triangle PR": 10,
           "Triangle OS": 11,
           "Triangle TY": 12
           }

algebra_keys = {}

physics_keys = {}

# Устанавливаем тайм-аут для всех запросов (например, 60 секунд)
# from telebot import apihelper
# apihelper.CONNECT_TIMEOUT = 120
# apihelper.READ_TIMEOUT = 120

# создание клавиатуры в сообщениях
def inline_keyboard(text_and_data_list, call_chat_id, type_of_figure = '', end_text='', msg='', media=''):
    keyboard = types.InlineKeyboardMarkup()
    print("idk")

    global text_to_analyse

    ms_id = "0"

    check_message(call_chat_id)
    chat_info = users_info[call_chat_id]

    buttons_list = []
    if not text_to_analyse:
        text_to_analyse = ["None", "None", "None", "None", "None"]


    for i in range(len(text_and_data_list)):
        buttons_list.append(types.InlineKeyboardButton(text=text_and_data_list[i][0], callback_data=text_and_data_list[i][1]))

    print(text_to_analyse[0])
    if text_to_analyse[0] != 'None':
        buttons_list.append(types.InlineKeyboardButton(text="назад", callback_data="BACK"))
    keyboard.add(*buttons_list)

    if end_text == '':
        end_text = type_and_its_text[type_of_figure]

    if users_info[call_chat_id] == "0":
        if media == '':
            if msg != "only start" and msg != "":
                ms_id = bot.send_message(call_chat_id, text=f"*{msg}*\n\n{end_text}", parse_mode="Markdown", reply_markup=keyboard)
            else:
                ms_id = bot.send_message(call_chat_id, text=end_text, reply_markup=keyboard)
        else:
            try:
                with open(media, 'rb') as photo:
                    ms_id = bot.send_photo(call_chat_id, photo=photo, caption=end_text, reply_markup=keyboard)
            except Exception as e:
                print(f"Ошибка при отправке: {e}")


def new_inline_keyboard(text_and_data_list, call_chat_id, end_text='', msg='', media=''):
    keyboard = types.InlineKeyboardMarkup()
    global text_to_analyse

    ms_id = "0"
    buttons_list = []

    if not text_to_analyse:
        text_to_analyse = ["None", "None", "None", "None", "None"]

    for i in range(len(text_and_data_list)):
        buttons_list.append(types.InlineKeyboardButton(text=text_and_data_list[i][0], callback_data=text_and_data_list[i][1]))
    keyboard.add(*buttons_list)

    return keyboard


# сброс данных о сообщениях одного пользователя
def list_clear(message):
    global users_info
    chat_id = message.from_user.id
    users_info[chat_id] = {}

def look_nice(text):
    def output():
        print("------------------------------",
              text,
              "------------------------------")
    return output()

# проверка, есть ли отправленные сообщения
def check_message(chat_id):
    # если пользователь есть в системе
    global users_info

    if chat_id in users_info:
        look_nice("YEAH")
        print(users_info)
    else:
        # если нет, то создаём такой элемент
        # ids_list.append(chat_id)
        users_info[chat_id] = {}

def message_layer_1(chat_id, new_text, info_type="", pic=''):
    global message_sended, ids_list

    chat_info = check_message(chat_id)
    bot.send_message(chat_id, text=chat_id)

    if info_type != "":
        type_list = message_sended[chat_info][geometry_keys[info_type]]
    else:
        bot.send_message(chat_id, new_text, parse_mode="Markdown")
        return
    print(type_list)

    if type_list[0] == False and type_list[1] == 0:
        if pic == '':
            try:
                bot_message = bot.send_message(chat_id, text=new_text, parse_mode="Markdown")
            except:
                bot.delete_message(chat_id=chat_id, message_id=type_list[1])
                bot_message = bot.send_message(chat_id, text=new_text, parse_mode="Markdown")
                type_list[1] = bot_message.message_id
                type_list[2] = chat_id
        else:
            bot_message = bot.send_photo(chat_id, photo=open(pic, 'rb'), caption=new_text, parse_mode="Markdown")
        type_list[0] = True
        type_list[1] = bot_message.message_id
        type_list[2] = chat_id
        message_sended[chat_info][geometry_keys[info_type]] = type_list

    elif type_list[0] == True or type_list[1] != 0:
        if pic == '':
            try:
                bot.edit_message_text(text=new_text, chat_id=chat_id, message_id=type_list[1], parse_mode="Markdown")
            except:
                bot.delete_message(chat_id=chat_id, message_id=type_list[1])
                bot_message = bot.send_message(text=new_text, chat_id=chat_id, parse_mode="Markdown")
                type_list[1] = bot_message.message_id
                type_list[2] = chat_id
        else:
            new_media = InputMediaPhoto(
                media=open(pic, 'rb'),
                caption=new_text,
                parse_mode="Markdown"
            )
            bot.edit_message_media(chat_id= chat_id,
                                   message_id=type_list[1],
                                   media=new_media)
        message_sended[chat_info][geometry_keys[info_type]] = type_list

    print(f"chat_info: {chat_info}")
    print(f"info_type: {info_type}")
    print(f"chat_id_state: {chat_id in ids_list}")
    print(f"ids_list: {ids_list}")
    print(f"chat_states: {message_sended[chat_info]}")

def message_layer(chat_id, new_text='', info_type="", pic='', keyboard_massive=[], msg='', page_type=[]):
    global message_sended, ids_list, arguments, new_message, pages

    check_message(chat_id)
    chat_info = users_info[chat_id]

    if not users_info or msg == "only start":
        new_message = True
        arguments = {}
        pages = {}
        users_info[chat_id]["pages_len"] = 0
        users_info[chat_id]['history_of_acts'] = ['None', 'None', 'None', 'None', 'None']
    else: new_message = False

    if not users_info[chat_id]["pages_len"]:
        keyboard_massive.append(["<-", "back"])

    try:
        # if keyboard_massive != ["<-", "back", "->", "next"]:
        arguments["reply_markup"] = new_inline_keyboard(keyboard_massive, chat_id, '', msg, '')

        if new_text != '':
            arguments["text"] = new_text
        else: arguments["text"] = type_and_its_text[info_type]

        if chat_id != 0:
            arguments["chat_id"] = chat_id

        if pic != '':
            arguments["timeout"] = 60
            if new_message == True:
                arguments["photo"] = open(pic, 'rb')

            new_media = InputMediaPhoto(
                media=open(pic, 'rb'),
                caption=arguments["text"],
                parse_mode="Markdown")
            arguments["media"] = new_media

            # print(arguments["media"])

        if page_type != []:
            if not pages[page_type]:
                pages[page_type] = users_info[chat_id]["pages_len"]
                users_info[chat_id]["pages_len"] += 1

        arguments["parse_mode"] = "Markdown"

        send_message(new_message, chat_id)

        print(users_info)

    except Exception as e:
        print(f"Ошибка при отправке: {e}")
        bot.send_message(chat_id, text="Сообщение для изменения не обнаружено")

    keyboard_massive.clear()

def send_message(new, chat_id):
    global arguments

    # Принудительно закрываем старую сессию, чтобы открылась новая
    # telebot.apihelper.CUSTOM_REQUESTER = session.post
    if new:
        if not arguments.get("media") and not arguments.get("photo"):
            arguments["message_id"] = bot.send_message(**arguments)

        elif arguments["media"].caption == "only start":
            arguments.pop("media", None)
            arguments["message_id"] = bot.send_message(**arguments)

        else:
            print("rrrr")
            reply = arguments["reply_markup"]
            arguments.pop("reply_markup", None)
            arguments["caption"] = arguments.pop("text")

            if arguments.get("media"):
                new_media = arguments["media"]
                arguments.pop("media", None)

            message_sent = bot.send_photo(**arguments)
            arguments["message_id"] = message_sent.message_id

            arguments["reply_markup"] = reply
            # arguments["text"] = arguments["caption"]
            print(arguments["message_id"])
            # new_media = InputMediaPhoto(
            #     media=open(pic, 'rb'),
            #     caption=arguments["caption"],
            #     parse_mode="Markdown"
            # )
            arguments["media"] = new_media

            arguments.pop("caption", None)
            arguments.pop('photo', None)
            arguments.pop('parse_mode', None)

            print(arguments)

            bot.edit_message_media(**arguments)

    else:
        text = arguments["text"]
        arguments.pop('text', None)
        arguments.pop('photo', None)
        arguments.pop('parse_mode', None)
        print(arguments)
        bot.edit_message_media(**arguments)
        arguments["text"] = text

    users_info[chat_id]["arguments"] = arguments

def choice(txt, chat_id):
    global keyboard_massive
    global text_to_analyse, users_info, history_id

    check_message(chat_id)

    text_to_analyse.clear()
    text_to_analyse.extend(txt.split())


    text_to_analyse.extend((5 - len(text_to_analyse)) * ["None"])

    print('ex:', text_to_analyse)

    history_of_acts = users_info[chat_id]['history_of_acts']

    print("FUCK", history_of_acts)

    if text_to_analyse[0] == 'back':
        num = 0
        print(*users_info[chat_id]['history_of_acts'])
        for item in users_info[chat_id]['history_of_acts']:
            if item == 'None':
                break
            num += 1

        # text_to_analyse = history_of_acts
        # text_to_analyse[num] = "None"
        users_info[chat_id]['history_of_acts'][num-1] = "None"
        print(text_to_analyse)
        print(users_info[chat_id]['history_of_acts'])
        print("num", num)
        history_of_acts = users_info[chat_id]['history_of_acts']
        print("----------------------", history_of_acts)

    elif text_to_analyse[0] != 'back':
        print('hhhhhhhhhhhh')
        history_of_acts = text_to_analyse.copy()
        users_info[chat_id]["history_of_acts"] = history_of_acts



    if history_of_acts[0] == "None":
        keyboard_massive = [['ТРЕУГОЛЬНИК', 'Triangle'],
                            ['ЧЕТЫРЁХУГОЛЬНИК', 'Geometry'],
                            ['ОКРУЖНОСТЬ И КРУГ', 'Circle'],
                            ['ПРЯМАЯ', 'Straight'],
                            ['УГОЛ', 'Corner']]
        message_layer(chat_id, geometry_OPR_text, "Geometry", 'приветствие.jpg', keyboard_massive)

    elif history_of_acts[0] == "Geometry":
            if history_of_acts[1] == "None":
                msg = "Сейчас я покажу, что я знаю о четырёхугольниках."

                keyboard_massive = [['ОБЩЕЕ', 'Geometry General'],
                                    ['ПРЯМОУГОЛЬНИК', 'Geometry Rectangle'],
                                    ['КВАДРАТ', 'Geometry Square'],
                                    ['ПАРАЛЛЕЛОГРАММ', 'Geometry Parallelogramm'],
                                    ['ТРАПЕЦИЯ', 'Geometry Trapezoid'],
                                    ['РОМБ', 'Geometry Rhomb'],
                                    ['ДЕЛЬТОИД', 'Geometry Deltoid']
                                    ]
                message_layer(chat_id, geometry_OPR_text, "Geometry", '4 четырёхугольник.png', keyboard_massive, msg)
                # inline_keyboard(keyboard_massive, call_chat_id=chat_id, msg=msg, type_of_figure="Geometry")

            elif history_of_acts[1] == "General":
                if history_of_acts[2] == "None":
                    msg = "Сейчас я покажу, что я знаю о прямоугольнике."

                    keyboard_massive = [['ОПРЕДЕЛЕНИЕ', 'Geometry General OPR'],
                                        ['СВОЙСТВА', 'Geometry General SV'],
                                        ['ПЛОЩАДЬ', 'Geometry General S'],
                                        ['ПРИЗНАКИ', 'Geometry General PR']
                                        ]
                    # inline_keyboard(keyboard_massive, call_chat_id=chat_id, msg=msg, type_of_figure="Geometry")
                    message_layer(chat_id, geometry_OPR_text, "Rectangle", '4 четырёхугольник.png', keyboard_massive, msg)

                elif history_of_acts[2] == "OPR":
                    message_layer(chat_id, geometry_OPR_text, "Rectangle", '4 четырёхугольник.png')
                elif history_of_acts[2] == "SV":
                    message_layer(chat_id, geometry_SV_text, "Rectangle", '4 четырёхугольник.png')
                elif history_of_acts[2] == "S":
                    message_layer(chat_id, geometry_S_text, "Rectangle", '4 четырёхугольник.png')
                elif history_of_acts[2] == "PR":
                    message_layer(chat_id, geometry_PR_text, "Rectangle", '4 четырёхугольник.png')

            elif history_of_acts[1] == "Rectangle":
                    if history_of_acts[2] == "None":
                        msg = "Сейчас я покажу, что я знаю о прямоугольнике."

                        keyboard_massive = [['СВОЙСТВА', 'Geometry Rectangle SV'],
                                            ['ПЛОЩАДЬ', 'Geometry Rectangle S'],
                                            ['ПРИЗНАКИ', 'Geometry Rectangle PR']
                                            ]

                        message_layer(chat_id, rect_OPR_text, "Rectangle", '4 прямоугольник.png', keyboard_massive, msg)

                    elif history_of_acts[2] == "SV":
                        message_layer(chat_id, rect_SV_text, "Rectangle", '4 прямоугольник.png')
                    elif history_of_acts[2] == "S":
                        message_layer(chat_id, rect_S_text, "Rectangle", '4 прямоугольник.png')
                    elif history_of_acts[2] == "PR":
                        message_layer(chat_id, rect_PR_text, "Rectangle", '4 прямоугольник.png')

            elif history_of_acts[1] == "Square":
                    if history_of_acts[2] == "None":
                        msg = "Сейчас я покажу, что я знаю о квадрате."

                        keyboard_massive = [['СВОЙСТВА', 'Geometry Square SV'],
                                            ['ПЛОЩАДЬ', 'Geometry Square S'],
                                            ['ПРИЗНАКИ', 'Geometry Square PR']
                                            ]
                        message_layer(chat_id, square_OPR_text, "Rectangle", '4 квадрат.jpg', keyboard_massive, msg)

                    elif history_of_acts[2] == "SV":
                        message_layer(chat_id, square_SV_text, "Rectangle", '4 квадрат.jpg')
                    elif history_of_acts[2] == "S":
                        message_layer(chat_id, square_S_text, "Rectangle", '4 квадрат.jpg')
                    elif history_of_acts[2] == "PR":
                        message_layer(chat_id, square_PR_text, "Rectangle", '4 квадрат.jpg')

            elif history_of_acts[1] == "Parallelogramm":
                    if history_of_acts[2] == "None":
                        msg = "Сейчас я покажу, что я знаю о квадрате."

                        keyboard_massive = [['СВОЙСТВА', 'Geometry Parallelogramm SV'],
                                            ['ПЛОЩАДЬ', 'Geometry Parallelogramm S'],
                                            ['ПРИЗНАКИ', 'Geometry Parallelogramm PR']]

                        message_layer(chat_id, parallelogr_OPR_text, "Rectangle",'4 параллелограмм.jpg', keyboard_massive, msg)

                    elif history_of_acts[2] == "SV":
                        message_layer(chat_id, parallelogr_SV_text, "Rectangle", '4 параллелограмм.jpg')
                    elif history_of_acts[2] == "S":
                        message_layer(chat_id, parallelogr_S_text, "Rectangle", '4 параллелограмм.jpg')
                    elif history_of_acts[2] == "PR":
                        message_layer(chat_id, parallelogr_PR_text, "Rectangle", '4 параллелограмм.jpg')

            elif history_of_acts[1] == 'Trapezoid':
                    if history_of_acts[2] == "None":
                        msg = "Сейчас я покажу, что я знаю о квадрате."

                        keyboard_massive = [['СВОЙСТВА', 'Geometry Trapezoid SV'],
                                            ['ПЛОЩАДЬ', 'Geometry Trapezoid S'],
                                            ['ПРИЗНАКИ', 'Geometry Trapezoid PR']
                                            ]
                        message_layer(chat_id, trapez_OPR_text, "Rectangle", '4 виды_трапеций.png', keyboard_massive, msg)

                    elif history_of_acts[2] == "SV":
                        message_layer(chat_id, trapez_SV_text, "Rectangle", '4 виды_трапеций.png')
                    elif history_of_acts[2] == "S":
                        message_layer(chat_id, trapez_S_text, "Rectangle", '4 виды_трапеций.png')
                    elif history_of_acts[2] == "PR":
                        message_layer(chat_id, trapez_PR_text, "Rectangle", '4 виды_трапеций.png')

            elif history_of_acts[1] == "Rhomb":
                    if history_of_acts[2] == "None":
                        msg = "Сейчас я покажу, что я знаю о квадрате."

                        keyboard_massive = [['СВОЙСТВА', 'Geometry Rhomb SV'],
                                            ['ПЛОЩАДЬ', 'Geometry Rhomb S'],
                                            ['ПРИЗНАКИ', 'Geometry Rhomb PR']
                                            ]
                        message_layer(chat_id, rhomb_OPR_text, "Rectangle", '4 ромб.png', keyboard_massive, msg)

                    elif history_of_acts[2] == "SV":
                        message_layer(chat_id, rhomb_SV_text, "Rectangle", '4 ромб.png')
                    elif history_of_acts[2] == "S":
                        message_layer(chat_id, rhomb_S_text, "Rectangle", '4 ромб.png')
                    elif history_of_acts[2] == "PR":
                        message_layer(chat_id, rhomb_PR_text, "Rectangle", '4 ромб.png')

            elif history_of_acts[1] == 'Deltoid':
                if history_of_acts[2] == "None":
                    msg = "Сейчас я покажу, что я знаю о квадрате."

                    keyboard_massive = [['СВОЙСТВА', 'Geometry Trapezoid SV'],
                                        ['ПЛОЩАДЬ', 'Geometry Trapezoid S'],
                                        ['ПРИЗНАКИ', 'Geometry Trapezoid PR']
                                        ]
                    message_layer(chat_id, deltoid_OPR_text, "Rectangle", '4 дельтоид.png', keyboard_massive, msg)

                elif history_of_acts[2] == "SV":
                    message_layer(chat_id, deltoid_SV_text, "Rectangle", '4 дельтоид.png')
                elif history_of_acts[2] == "S":
                    message_layer(chat_id, deltoid_S_text, "Rectangle", '4 дельтоид.png')
                elif history_of_acts[2] == "PR":
                    message_layer(chat_id, deltoid_PR_text, "Rectangle", '4 дельтоид.png')

    elif history_of_acts[0] == 'Circle':
            if history_of_acts[1] == "None":
                msg = "Сейчас я покажу, что я знаю о окружностях и кругах."

                keyboard_massive = [['КРУГ', 'Circle Kr'],
                                    ['ОКРУЖНОСТЬ', 'Circle OK'],
                                    ['ХОРДА', 'Circle Ln']]
                message_layer(chat_id, keyboard_massive=keyboard_massive, msg=msg)

            elif history_of_acts[1] == "Kr":
                message_layer(chat_id, circle_kr_text, "Circle", '')

            elif history_of_acts[1] == "OK":

                if history_of_acts[2] == "None":
                    msg = "Что хочешь узнать об окружности?"
                    keyboard_massive = [['ОПРЕДЕЛЕНИЕ', 'Circle OK OPR'],
                                        ['ДИАМЕТР', 'Circle OK D'],
                                        ['РАДИУС', 'Circle OK R'],
                                        ['СВОЙСТВА', 'Circle OK SV']
                                        ]
                    inline_keyboard(keyboard_massive, call_chat_id=chat_id, msg=msg)

                elif history_of_acts[2] == 'OPR':
                    message_layer(chat_id, circle_ok_OPR_text, "Circle OK", '')

                elif history_of_acts[2] == 'D':
                    message_layer(chat_id, circle_ok_D_text, "Circle OK", '1 диаметр окружности.png')

                elif history_of_acts[2] == 'R':
                    message_layer(chat_id, circle_ok_R_text, "Circle OK", '1 радиус окружности.png')

                elif history_of_acts[2] == 'SV':
                    message_layer(chat_id, circle_ok_SV_text, "Circle OK", '')

            elif history_of_acts[1] == 'Ln':
                    if history_of_acts[2] == "None":
                        keyboard_massive = [['ХОРДА', 'Circle Ln H'],
                                            ['ДУГА', 'Circle Ln Dg'],
                                            ['КАСАТЕЛЬНАЯ', 'Circle Ln Ks'],
                                            ]
                        message_layer(chat_id, keyboard_massive=keyboard_massive, msg="Тут просто линии")

                    elif history_of_acts[2] == 'H':
                            if history_of_acts[3] == "None":
                                keyboard_massive = [['ОПРЕДЕЛЕНИЕ', 'Circle Ln H OPR'],
                                                    ['СВОЙСТВА', 'Circle Ln H SV'],
                                                    ]
                                message_layer(chat_id, keyboard_massive=keyboard_massive, msg="Тут про хорду")

                            elif history_of_acts[3] == 'OPR':
                                message_layer(chat_id, circle_ln_H_OPR_text, "Circle Ln H", '1 определение хорды.png')

                            elif history_of_acts[3] == 'SV':
                                message_layer(chat_id, circle_ln_H_SV_text, "Circle Ln H", '')

                    elif history_of_acts[2] == 'Dg':
                        message_layer(chat_id, circle_ln_Dg_text, "Circle Ln", '1 определение дуги.png')

                    elif history_of_acts[2] == 'Ks':
                            if history_of_acts[3] == "None":
                                keyboard_massive = [['ОПРЕДЕЛЕНИЕ', 'Circle Ln Ks OPR'],
                                                    ['СВОЙСТВА', 'Circle Ln Ks SV'],
                                                    ['ТЕОРЕМА', 'Circle Ln Ks TH']
                                                    ]
                                message_layer(chat_id, keyboard_massive=keyboard_massive, msg="Информация про касательную линию")

                            elif history_of_acts[3] == 'OPR':
                                message_layer(chat_id, circle_ln_Ks_OPR_text, "Circle Ln Ks", '1 определение касательной.png')

                            elif history_of_acts[3] == 'SV':
                                message_layer(chat_id, circle_ln_Ks_SV_text, "Circle Ln Ks", '')

                            elif history_of_acts[3] == 'TH':
                                message_layer(chat_id, circle_ln_Ks_TH_text, "Circle Ln Ks", '')

    elif history_of_acts[0] == "Straight":
            if history_of_acts[1] == "None":
                msg = "Сейчас я покажу, что я знаю о прямых."

                keyboard_massive = [['ПАРАЛЛЕЛЬНЫЕ', 'Straight Pa'],
                                    ['ПЕРПЕНДИКУЛЯРНЫЕ', 'Straight Pe']]

                message_layer(chat_id, keyboard_massive=keyboard_massive, msg=msg)

            elif history_of_acts[1] == "Pa":
                message_layer(chat_id, straight_PA_text, "Straight", '')

            elif history_of_acts[1] == "Pe":
                message_layer(chat_id, straight_Pe_text, "Straight", '')

    elif history_of_acts[0] == "Corner":
            if history_of_acts[1] == "None":
                msg = "Сейчас я покажу, что я знаю о углах."

                keyboard_massive = [['ВЕРТИКАЛЬНЫЕ УГЛЫ', 'Corner Ve'],
                                    ['СМЕЖНЫЕ УГЛЫ', 'Corner Sm'],
                                    ['ДВЕ ПРЯМЫЕ И СЕКУЩАЯ', 'Corner Pe']]

                message_layer(chat_id, keyboard_massive=keyboard_massive, msg=msg)

            elif history_of_acts[1] == "Ve":
                message_layer(chat_id, corner_Ve_text, "Corner", '2 вертикальные.png')

            elif history_of_acts[1] == "Sm":
                message_layer(chat_id, corner_Sm_text, "Corner", '2 смежные.png')

            elif history_of_acts[1] == "Pe":
                    if history_of_acts[2] == "None":
                        msg = "Сейчас я покажу, что я знаю о пересечении двух прямых секущей."

                        keyboard_massive = [['Соответственные углы', 'Corner Pe So'],
                                            ['накрест лежащие углы', 'Corner Pe Na'],
                                            ['Односторонние углы', 'Corner Pe Od']]

                        message_layer(chat_id, keyboard_massive=keyboard_massive, msg=msg)

                    elif history_of_acts[2] == "So":
                        message_layer(chat_id, corner_So_text, "Corner PE", '2 соответственные.png')

                    elif history_of_acts[2] == "Na":
                        message_layer(chat_id, corner_Na_text, "Corner PE", '2 накрест лежащие.png')

                    elif history_of_acts[2] == "Od":
                        message_layer(chat_id, corner_Od_text, "Corner PE", '2 односторонние.png')

    elif history_of_acts[0] == "Triangle":
            if history_of_acts[1] == "None":
                msg = "Сейчас я покажу, что я знаю о треугольниках."

                keyboard_massive = [['ПРЯМОУГОЛЬНЫЙ ТРЕУГОЛЬНИК', 'Triangle PR'],
                                      ['ОСТРОУГОЛЬНЫЙ ТРЕУГОЛЬНИК', 'Triangle OS'],
                                      ['ТУПОУГОЛЬНЫЙ ТРЕУГОЛЬНИК', 'Triangle TY']]
                message_layer(chat_id, keyboard_massive=keyboard_massive, pic='3 рб треугольник.png', msg=msg)

            elif history_of_acts[1] == "PR":
                    if text_to_analyse[2] == "None":
                        keyboard_massive = [['БИССЕКТРИСА', 'Triangle PR B'],
                                            ['МЕДИАНА', 'Triangle PR M'],
                                            ['ВЫСОТА', 'Triangle PR V'],
                                            ['ПРИЗНАКИ РАВЕНСТВА', 'Triangle PR R'],
                                            ['РАВНОБЕДРЕННОСТЬ', 'Triangle PR RB']]

                        message_layer(chat_id, keyboard_massive=keyboard_massive, msg="Выбери что ты хочешь узнать о прямоугольном треугольнике:")

                    elif history_of_acts[2] == "B":
                        message_layer(chat_id, triangle_PrB_text, "Triangle PR", '')

                    elif history_of_acts[2] == "M":
                        message_layer(chat_id, triangle_PrM_text, "Triangle PR", '')

                    elif history_of_acts[2] == "V":
                        message_layer(chat_id, triangle_PrV_text, "Triangle PR", '')

                    elif history_of_acts[2] == "R":
                        message_layer(chat_id, triangle_PrR_text, "Triangle PR", '')

                    elif history_of_acts[2] == "RB":
                        message_layer(chat_id, triangle_PrRB_text, "Triangle PR", '')

            elif history_of_acts[1] == "OS":
                    if text_to_analyse[2] == "None":
                        msg = "Сейчас я покажу, что я знаю об остроугольных треугольных."

                        keyboard_massive = [['БИССИКТРИСА', 'Triangle OS B'],
                                            ['МЕДИАНА', 'Triangle OS M'],
                                            ['ВЫСОТА', 'Triangle OS V'],
                                            ['ПРИЗНАКИ РАВЕНСТВА', 'Triangle OS R'],
                                            ['РАВНОБЕДРЕННОСТЬ', 'Triangle OS RB'],
                                            ['РАВНОСТОРОННОСТЬ', 'Triangle OS RS']
                                            ]
                        message_layer(chat_id, keyboard_massive=keyboard_massive, msg=msg)

                    elif history_of_acts[2] == "B":
                        message_layer(chat_id, triangle_OSB_text, "Triangle OS", '')

                    elif history_of_acts[2] == "M":
                        message_layer(chat_id, triangle_OSM_text, "Triangle OS", '')

                    elif history_of_acts[2] == "V":
                        message_layer(chat_id, triangle_OSV_text, "Triangle OS", '')

                    elif history_of_acts[2] == "R":
                        message_layer(chat_id, triangle_OSR_text, "Triangle OS", '')

                    elif history_of_acts[2] == "RB":
                        message_layer(chat_id, triangle_OSRB_text, "Triangle OS", '')

                    elif history_of_acts[2] == "RS":
                        message_layer(chat_id, triangle_OSRS_text, "Triangle OS", '')

            elif history_of_acts[1] == "TY":
                if history_of_acts[2] == "None":
                    msg = "Сейчас я покажу, что я знаю о тупогольных треугольных."

                    keyboard_massive = [['БИССИКТРИСА', 'Triangle TY B'],
                                        ['МЕДИАНА', 'Triangle TY M'],
                                        ['ВЫСОТА', 'Triangle TY V'],
                                        ['ПРИЗНАКИ РАВЕНСТВА', 'Triangle TY R'],
                                        ['РАВНОБЕДРЕННОСТЬ', 'Triangle TY RB']
                                        ]
                    message_layer(chat_id, keyboard_massive=keyboard_massive, msg=msg)

                elif history_of_acts[2] == "B":
                    message_layer(chat_id, triangle_TYB_text, "Triangle TY", '')

                elif history_of_acts[2] == "M":
                    message_layer(chat_id, triangle_TYM_text, "Triangle TY", '')

                elif history_of_acts[2] == "V":
                    message_layer(chat_id, triangle_TYV_text, "Triangle TY", '')

                elif history_of_acts[2] == "R":
                    message_layer(chat_id, triangle_TYR_text, "Triangle TY", '')

                elif history_of_acts[2] == "RB":
                    message_layer(chat_id, triangle_TYRB_text, "Triangle TY", '')

    else:
        message_layer(chat_id, "Я тебя не понимаю. Напиши /help.", "", '')

    print("nu vot:", text_to_analyse)
    print("nu vot v2:", users_info[chat_id]["history_of_acts"])
    users_info[chat_id]["history_of_acts"] = history_of_acts
