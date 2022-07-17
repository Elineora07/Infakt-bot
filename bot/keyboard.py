import telebot
from telebot.types import *


bot = telebot.TeleBot("token qo'yiladi")


def start_register_keyboard(data):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("Ro'yxatdan o'tish")
    return keyboard.add(btn)


def register_update_inline_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("Ism", callback_data="register_update_inline_keyboard__first_name")
    btn2 = InlineKeyboardButton("Familiya", callback_data="register_update_inline_keyboard__last_name")
    btn3 = InlineKeyboardButton("Sharif", callback_data="register_update_inline_keyboard__middle_name")
    btn4 = InlineKeyboardButton("Telefon raqam", callback_data="register_update_inline_keyboard__phone")
    return keyboard.add(btn1, btn2, btn3, btn4)
