import telebot
from telebot.types import *

bot = telebot.TeleBot("token qo'iladi")


data = {
    "user": {},
    "admin": [id raqam],
    "type": {}
}


def get_keyboard():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("Ro'yxatdan o'tish")
    )


def get_inlinekeyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    first_name = InlineKeyboardButton("Ism", callback_data="first_name+1")
    last_name = InlineKeyboardButton("Familiya", callback_data="last_name+1")
    phone = InlineKeyboardButton('Telefon nomer', callback_data="phone+1")
    return keyboard.add(first_name, last_name, phone)


def update_type(message):
    user_id = message.chat.id
    user_type = data['type'][user_id]
    text = message.text
    if user_type == 'phone':
        if text.startswith("+998") and len(text) == 13 and text[1:].isdigit():
            data["user"][user_id][user_type] = message.text
            bot.send_message(user_id, "Sizning kiritgan malumotigiz qabul qilindi")
        else:
            bot.send_message(user_id, "Boshqatdan telefon nomerni kiriting")
            bot.register_next_step_handler(message, update_type)
    else:
        if text.isalpha():
            data["user"][user_id][user_type] = message.text
            bot.send_message(user_id, "Sizning kiritgan malumotigiz qabul qilindi")
        else:
            type = {
                "first_name": "Ism",
                "last_name": "Familiya"
            }
            bot.send_message(user_id, f"Boshqatdan {type[user_type]} kiriting")
            bot.register_next_step_handler(message, update_type)



@bot.callback_query_handler(func=lambda x: x.data.split("+")[-1] == "1")
def update_user_data(call):
    type_user = call.data.split("+")[0]
    user_id = call.message.chat.id
    data['type'][user_id] = type_user
    type = {
        "first_name": "Ism",
        "last_name": "Familiya",
        "phone": "Telefon nomer"
    }
    bot.edit_message_text(
        f"{type[type_user]} kiriting",
        call.message.chat.id,
        call.message.id
    )
    bot.register_next_step_handler(call.message, update_type)


def data_text(message):
    user_data = data["user"][message.chat.id]
    print(user_data)
    if user_data:
        text = f"Ism: {user_data['first_name']}\n" \
               f"Familiya: {user_data['last_name']}\n" \
               f"Telefon nomer: {user_data['phone']}"
        return text
    data["user"][message.chat.id] = {
        "first_name": "-",
        "last_name": "-",
        "phone": "-"
    }
    return "Ism: -\n" \
           "Familiya: -\n" \
           "Telefon nomer: -"


@bot.message_handler(func=lambda x: x.text == "Ro'yxatdan o'tish")
def registration(message):
    text = data_text(message)
    bot.send_message(message.chat.id, f"{text}", reply_markup=get_inlinekeyboard())


@bot.message_handler(commands="start")
def start(message):
    print(message.chat.id)
    if message.chat.id in data["admin"]:
        bot.send_message(message.chat.id, f"salom {message.from_user.first_name}", reply_markup=admin_keyboard())
    else:
        if message.chat.id not in data['user']:
            data["user"][message.chat.id] = {}
        bot.send_message(message.chat.id, f"salom {message.from_user.first_name}", reply_markup=get_keyboard())


def admin_keyboard():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("Ro'yxat")
    )


bot.polling()
