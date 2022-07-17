import telebot
from telebot.types import *
from keyboard import start_register_keyboard, register_update_inline_keyboard
from text import register_text

bot = telebot.TeleBot("token qo'yiladi")


data = {
    "user": {},
    "admin": [id raqam],
    "photo": []
}
def location(message):
    print(message.location)
    latitude = message.location.latitude
    longitude = message.location.longitude
    bot.send_location(message.chat.id, latitude, longitude)


@bot.message_handler(func=lambda x: x.text == "Location")
def location_update(message):
    user_id = message.chat.id
    if user_id in data['admin']:
        bot.send_message(user_id, "location kiriting")
        bot.register_next_step_handler(message, location)




def add_rasm(message):
    photo = message.photo[-1]
    photo = photo.file_id
    data['photo'] = data['photo'].append(photo)
    bot.send_photo(message.chat.id, photo, caption="salomasomads")


@bot.message_handler(func=lambda x: x.text == "Rasm")
def rasm(message):
    user_id = message.chat.id
    bot.send_message(user_id, "rasm jo'nat")
    bot.register_next_step_handler(message, add_rasm)














def admin_add_function(message):
    new_admin = message.forward_from.id
    data['admin'] = data['admin'] + [new_admin]
    print(data['admin'])


@bot.message_handler(func=lambda x: x.text == "Admin")
def admin_add(message):
    user_id = message.chat.id
    if user_id in data['admin']:
        bot.send_message(user_id, 'admindan birorta nasrsa forward qiling')
        bot.register_next_step_handler(message, admin_add_function)



def admin_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = KeyboardButton("Rasm")
    btn2 = KeyboardButton("Location")
    btn3 = KeyboardButton("Admin")
    return keyboard.add(btn1, btn2, btn3)

##############################3


def update_name(message):
    name = message.text
    user_id = message.chat.id
    type_name = data['user'][user_id]['type']
    if name != "Ro'yxatdan o'tish":
        data['user'][user_id][type_name] = name
        bot.send_message(user_id, register_text(user_id, data), reply_markup=register_update_inline_keyboard())
    elif name == "Ro'yxatdan o'tish":
        text = register_text(user_id, data)
        bot.send_message(user_id, text, reply_markup=register_update_inline_keyboard())


def call_update_name(user_id, type_name, message):
    text = {
        "first_name": "Ism",
        "last_name": "Familiya",
        "middle_name": "Sharif",
        "phone": "Telfon raqam"
    }
    bot.edit_message_text(
        f"{text[type_name]}ni kiriting",
        user_id,
        message.id
        )
    bot.register_next_step_handler(message, update_name)


@bot.callback_query_handler(func=lambda x: x.data.split("__")[0] == "register_update_inline_keyboard")
def update(call):
    type_name = call.data.split("__")[1]
    user_id = call.message.chat.id
    data['user'][user_id]['type'] = type_name
    call_update_name(user_id, type_name, call.message)


@bot.message_handler(func=lambda x: x.text == "Ro'yxatdan o'tish")
def register(message):
    user_id = message.chat.id
    if user_id not in data['user']:
        data["user"][user_id] = {
            "first_name": f"{message.chat.first_name}",
            "last_name": "-",
            "middle_name": "-",
            "phone": "-",
            "type": ""
        }
    text = register_text(user_id, data)
    bot.send_message(user_id, text, reply_markup=register_update_inline_keyboard())


@bot.message_handler(commands="start")
def start(message):
    user_id = message.chat.id
    if user_id not in data['admin']:
        bot.send_message(user_id, f"Salom {message.chat.first_name}", reply_markup=start_register_keyboard(data))
    else:
        bot.send_message(user_id, "salom admin", reply_markup=admin_keyboard())


bot.polling()
