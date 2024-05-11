# - *- coding: utf- 8 - *-
import random
import time
import uuid
from datetime import datetime
from typing import Union

import pytz
from aiogram import Bot
from aiogram.types import InlineKeyboardButton, KeyboardButton, WebAppInfo, Message, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup

from tgbot.data.config import get_admins, BOT_TIMEZONE


######################################## AIOGRAM ########################################
# Генерация реплай кнопки
def rkb(text: str) -> KeyboardButton:
    return KeyboardButton(text=text)


# Генерация инлайн кнопки
def ikb(text: str, data: str = None, url: str = None, switch: str = None, web: str = None) -> InlineKeyboardButton:
    if data is not None:
        return InlineKeyboardButton(text=text, callback_data=data)
    elif url is not None:
        return InlineKeyboardButton(text=text, url=url)
    elif switch is not None:
        return InlineKeyboardButton(text=text, switch_inline_query=switch)
    elif web is not None:
        return InlineKeyboardButton(text=text, web_app=WebAppInfo(url=web))


# Удаление сообщения с обработкой ошибки от телеграма
async def del_message(message: Message):
    try:
        await message.delete()
    except:
        ...


# Умная отправка сообщений (автоотправка сообщения с фото или без)
async def smart_message(
        bot: Bot,
        user_id: int,
        text: str,
        keyboard: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup] = None,
        photo: Union[str, None] = None,
):
    if photo is not None and photo.title() != "None":
        await bot.send_photo(
            chat_id=user_id,
            photo=photo,
            caption=text,
            reply_markup=keyboard,
        )
    else:
        await bot.send_message(
            chat_id=user_id,
            text=text,
            reply_markup=keyboard,
        )


# Отправка сообщения всем админам
async def send_admins(bot: Bot, text: str, markup=None, not_me=0):
    for admin in get_admins():
        try:
            if str(admin) != str(not_me):
                await bot.send_message(
                    admin,
                    text,
                    reply_markup=markup,
                    disable_web_page_preview=True,
                )
        except:
            ...


######################################## ПРОЧЕЕ ########################################
# Удаление отступов в многострочной строке ("""text""")
def ded(get_text: str) -> str:
    if get_text is not None:
        split_text = get_text.split("\n")
        if split_text[0] == "": split_text.pop(0)
        if split_text[-1] == "": split_text.pop()
        save_text = []

        for text in split_text:
            while text.startswith(" "):
                text = text[1:].strip()

            save_text.append(text)
        get_text = "\n".join(save_text)
    else:
        get_text = ""

    return get_text


# Очистка текста от HTML тэгов ('<b>test</b>' -> *b*test*/b*)
def clear_html(get_text: str) -> str:
    if get_text is not None:
        if "</" in get_text: get_text = get_text.replace("<", "*")
        if "<" in get_text: get_text = get_text.replace("<", "*")
        if ">" in get_text: get_text = get_text.replace(">", "*")
    else:
        get_text = ""

    return get_text


# Очистка пробелов в списке (['', 1, ' ', 2] -> [1, 2])
def clear_list(get_list: list) -> list:
    while "" in get_list: get_list.remove("")
    while " " in get_list: get_list.remove(" ")
    while "." in get_list: get_list.remove(".")
    while "," in get_list: get_list.remove(",")
    while "\r" in get_list: get_list.remove("\r")
    while "\n" in get_list: get_list.remove("\n")

    return get_list


# Разбив списка на несколько частей ([1, 2, 3, 4] 2 -> [[1, 2], [3, 4]])
def split_list(get_list: list, count: int) -> list[list]:
    return [get_list[i:i + count] for i in range(0, len(get_list), count)]


# Получение текущей даты (True - дата с временем, False - дата без времени)
def get_date(full: bool = True) -> str:
    if full:
        return datetime.now(pytz.timezone(BOT_TIMEZONE)).strftime("%d.%m.%Y %H:%M:%S")
    else:
        return datetime.now(pytz.timezone(BOT_TIMEZONE)).strftime("%d.%m.%Y")


# Получение текущего unix времени (True - время в наносекундах, False - время в секундах)
def get_unix(full: bool = False) -> int:
    if full:
        return time.time_ns()
    else:
        return int(time.time())


# Конвертация unix в дату и даты в unix
def convert_date(from_time, full=True, second=True) -> Union[str, int]:
    from tgbot.data.config import BOT_TIMEZONE

    if "-" in str(from_time):
        from_time = from_time.replace("-", ".")

    if str(from_time).isdigit():
        if full:
            to_time = datetime.fromtimestamp(from_time, pytz.timezone(BOT_TIMEZONE)).strftime("%d.%m.%Y %H:%M:%S")
        elif second:
            to_time = datetime.fromtimestamp(from_time, pytz.timezone(BOT_TIMEZONE)).strftime("%d.%m.%Y %H:%M")
        else:
            to_time = datetime.fromtimestamp(from_time, pytz.timezone(BOT_TIMEZONE)).strftime("%d.%m.%Y")
    else:
        if " " in str(from_time):
            cache_time = from_time.split(" ")

            if ":" in cache_time[0]:
                cache_date = cache_time[1].split(".")
                cache_time = cache_time[0].split(":")
            else:
                cache_date = cache_time[0].split(".")
                cache_time = cache_time[1].split(":")

            if len(cache_date[0]) == 4:
                x_year, x_month, x_day = cache_date[0], cache_date[1], cache_date[2]
            else:
                x_year, x_month, x_day = cache_date[2], cache_date[1], cache_date[0]

            x_hour, x_minute, x_second = cache_time[0], cache_time[1], cache_time[2]

            from_time = f"{x_day}.{x_month}.{x_year} {x_hour}:{x_minute}:{x_second}"
        else:
            cache_date = from_time.split(".")

            if len(cache_date[0]) == 4:
                x_year, x_month, x_day = cache_date[0], cache_date[1], cache_date[2]
            else:
                x_year, x_month, x_day = cache_date[2], cache_date[1], cache_date[0]

            from_time = f"{x_day}.{x_month}.{x_year}"

        if " " in str(from_time):
            to_time = int(datetime.strptime(from_time, "%d.%m.%Y %H:%M:%S").timestamp())
        else:
            to_time = int(datetime.strptime(from_time, "%d.%m.%Y").timestamp())

    return to_time


# Генерация уникального айди
def gen_id(len_id: int = 16) -> int:
    mac_address = uuid.getnode()
    time_unix = int(str(time.time_ns())[:len_id])
    random_int = int(''.join(random.choices('0123456789', k=len_id)))

    return mac_address + time_unix + random_int


# Генерация пароля | default, number, letter, onechar
def gen_password(len_password: int = 16, type_password: str = "default") -> str:
    if type_password == "default":
        char_password = list("1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ")
    elif type_password == "letter":
        char_password = list("abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ")
    elif type_password == "number":
        char_password = list("1234567890")
    elif type_password == "onechar":
        char_password = list("1234567890")

    random.shuffle(char_password)
    random_chars = "".join([random.choice(char_password) for x in range(len_password)])

    if type_password == "onechar":
        random_chars = f"{random.choice('abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ')}{random_chars[1:]}"

    return random_chars


# Дополнение к числу корректного времени (1 -> 1 день, 3 -> 3 дня)
def convert_times(get_time: int, get_type: str = "day") -> str:
    get_time = int(get_time)
    if get_time < 0: get_time = 0

    if get_type == "second":
        get_list = ['секунда', 'секунды', 'секунд']
    elif get_type == "minute":
        get_list = ['минута', 'минуты', 'минут']
    elif get_type == "hour":
        get_list = ['час', 'часа', 'часов']
    elif get_type == "day":
        get_list = ['день', 'дня', 'дней']
    elif get_type == "month":
        get_list = ['месяц', 'месяца', 'месяцев']
    else:
        get_list = ['год', 'года', 'лет']

    if get_time % 10 == 1 and get_time % 100 != 11:
        count = 0
    elif 2 <= get_time % 10 <= 4 and (get_time % 100 < 10 or get_time % 100 >= 20):
        count = 1
    else:
        count = 2

    return f"{get_time} {get_list[count]}"


# Проверка на булевый тип
def is_bool(value: Union[bool, str, int]) -> bool:
    value = str(value).lower()

    if value in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif value in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        raise ValueError(f"invalid truth value {value}")


######################################## ЧИСЛА ########################################
# Преобразование экспоненциальных чисел в читаемый вид (1e-06 -> 0.000001)
def snum(amount: Union[int, float], remains: int = 2) -> str:
    format_str = "{:." + str(remains) + "f}"
    str_amount = format_str.format(float(amount))

    if remains != 0:
        if "." in str_amount:
            remains_find = str_amount.find(".")
            remains_save = remains_find + 8 - (8 - remains) + 1

            str_amount = str_amount[:remains_save]

    if "." in str(str_amount):
        while str(str_amount).endswith('0'): str_amount = str(str_amount)[:-1]

    if str(str_amount).endswith('.'): str_amount = str(str_amount)[:-1]

    return str(str_amount)


# Конвертация любого числа в вещественное, с удалением нулей в конце (remains - округление)
def to_float(get_number, remains: int = 2) -> Union[int, float]:
    if "," in str(get_number):
        get_number = str(get_number).replace(",", ".")

    if "." in str(get_number):
        get_last = str(get_number).split(".")

        if str(get_last[1]).endswith("0"):
            while True:
                if str(get_number).endswith("0"):
                    get_number = str(get_number)[:-1]
                else:
                    break

        get_number = round(float(get_number), remains)

    str_number = snum(get_number)
    if "." in str_number:
        if str_number.split(".")[1] == "0":
            get_number = int(get_number)
        else:
            get_number = float(get_number)
    else:
        get_number = int(get_number)

    return get_number


# Конвертация вещественного числа в целочисленное
def to_int(get_number: float) -> int:
    if "," in get_number:
        get_number = str(get_number).replace(",", ".")

    get_number = int(round(float(get_number)))

    return get_number


# Проверка ввода на число
def is_number(get_number: Union[str, int, float]) -> bool:
    if str(get_number).isdigit():
        return True
    else:
        if "," in str(get_number): get_number = str(get_number).replace(",", ".")

        try:
            float(get_number)
            return True
        except ValueError:
            return False


# Преобразование числа в читаемый вид (123456789 -> 123 456 789)
def format_rate(amount: Union[float, int], around: int = 2) -> str:
    if "," in str(amount): amount = float(str(amount).replace(",", "."))
    if " " in str(amount): amount = float(str(amount).replace(" ", ""))
    amount = str(round(amount, around))

    out_amount, save_remains = [], ""

    if "." in amount: save_remains = amount.split(".")[1]
    save_amount = [char for char in str(int(float(amount)))]

    if len(save_amount) % 3 != 0:
        if (len(save_amount) - 1) % 3 == 0:
            out_amount.extend([save_amount[0]])
            save_amount.pop(0)
        elif (len(save_amount) - 2) % 3 == 0:
            out_amount.extend([save_amount[0], save_amount[1]])
            save_amount.pop(1)
            save_amount.pop(0)
        else:
            print("Error 4388326")

    for x, char in enumerate(save_amount):
        if x % 3 == 0: out_amount.append(" ")
        out_amount.append(char)

    response = "".join(out_amount).strip() + "." + save_remains

    if response.endswith("."):
        response = response[:-1]

    return response
