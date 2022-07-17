import telebot
from telebot.types import *


bot = telebot.TeleBot("token qo'yiladi")


data = {
    "event": {
        1: ['ashdajksdhasd', 'AgACAgIAAxkBAAIRnmHnKgH5ZjyisUr8LsJkmqSvoDkcAAJ7uDEbSBM5S7WzWJMB4A4eAQADAgADeQADIwQ'],
        2: ['gsdfgdsfgdfgdsfg', 'AgACAgIAAxkBAAIRnmHnKgH5ZjyisUr8LsJkmqSvoDkcAAJ7uDEbSBM5S7WzWJMB4A4eAQADAgADeQADIwQ']
    },
    "event_user": {},
    "registration": {},
    "admin": [id raqam],
    "admin_number": [],
    "users": {},
    "location": {},
    "phone": ["tel nomer"],
    "event_sum": 1,
    "type": {},
    "user_event": {},
    "photo_id": 0
}


def create(message):
    if message.test == "Tadbirlar":
        bot.send_message(message.chat.id, event(), reply_markup=keyboard_admin_event_meny())
    elif message.test == "Manzil":
        bot.send_message(message.chat.id, "Yengi manzil kiriting")
        bot.register_next_step_handler(message, create_location)
    elif message.test == "Telefon nomer":
        bot.send_message(message.chat.id, "Iltimos malumot kiriting")
        bot.register_next_step_handler(message, create)
    elif message.test == "Admin":
        bot.send_message(message.chat.id, "Iltimos qo'shmoqchi bo'lgan admindan bitta habarni forward qiling")
        bot.register_next_step_handler(message, add_new_admin)
    else:
        data['phone'] = message.test
        bot.send_message(message.chat.id, "Malumot qo'shildi")


def add_new_admin(message):
    if message.forward_from:
        new_admin_id = message.forward_from.id
        data["admin"] = data["admin"] + [new_admin_id]
        bot.send_message(message.chat.id, "Yengi admin qo'shildi")
    elif message.test == "Tadbirlar":
        bot.send_message(message.chat.id, event(), reply_markup=keyboard_admin_event_meny())
    elif message.test == "Manzil":
        bot.send_message(message.chat.id, "Yengi manzil kiriting")
        bot.register_next_step_handler(message, create_location)
    elif message.test == "Telefon nomer":
        bot.send_message(message.chat.id, "Iltimos malumot kiriting")
        bot.register_next_step_handler(message, create)



    elif message.test == "Admin":
        bot.send_message(message.chat.id, "Iltimos qo'shmoqchi bo'lgan admindan bitta habarni forward qiling")
        bot.register_next_step_handler(message, add_new_admin)
    else:
        bot.send_message(message.chat.id, "Admin qo'shilmadi.\nIltimos yengi admindan bitta habarini forward qilin")


"""------------ user lavozim qatori -----------"""


@bot.callback_query_handler(func=lambda x: 'position_' in x.data)
def update_position(call):
    type = call.data.split("_")[1]
    data["users"][call.message.chat.id]['position'] = type
    bot.edit_message_text(
        user_my_profile_create(call.message),
        call.message.chat.id,
        call.message.id,
        reply_markup=keyboard_user_my_profile()
    )


def position_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("Biznis egasi(tasischi)", callback_data="position_Biznis egasi(tasischi)")
    btn2 = InlineKeyboardButton("Kompaniya rahbari", callback_data="position_Kompaniya rahbari")
    btn3 = InlineKeyboardButton("Marketing/Savdo bulimi boshlig'i", callback_data="position_Marketing/Savdo bulimi boshlig'i")
    btn4 = InlineKeyboardButton("Marketing/Savdo bulimi hodimi", callback_data="position_Marketing/Savdo bulimi hodimi")
    btn5 = InlineKeyboardButton("Stajor(talaba)", callback_data="position_Stajor(talaba)")
    btn6 = InlineKeyboardButton("Tashkilot hodimi", callback_data="position_Tashkilot hodimi")
    btn7 = InlineKeyboardButton("Ish boshqaruvchi", callback_data="position_Ish boshqaruvchi")
    return keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)


@bot.callback_query_handler(func=lambda x: x.data == "position")
def position(call):
    bot.edit_message_text(
        "🔹 Lavozimngizni tanlang? 👇",
        call.message.chat.id,
        call.message.id,
        reply_markup=position_keyboard()
    )


"""----------- user korxona nomi qatori --------------------------"""


def update_name_enterprise(message):
    new_name = message.text
    if message.text == "🔖 Tadbirlar":
        text = "Muvoffaqiyat tajriba natijasi\n" \
               "Tajriba-mag'lubiyatlar natojasi\n\n" \
               "Har bosib o'tilgan yol, o'z izini qoldiradi"
        bot.send_message(message.chat.id, text, reply_markup=keyboard_user_event())
    elif message.text == "👤 Mening profilim":
        bot.send_message(message.chat.id, user_my_profile_create(message), reply_markup=keyboard_user_my_profile())
    elif message.text == "📞 Admin bilan bog'lanish":
        if data["phone"]:
            text = ""
            for s in data["phone"]:
                text += s + "\n"
            bot.send_message(message.chat.id, text, reply_markup=get_keyboard_link())
        else:
            bot.send_message(message.chat.id, "Uzur hozircha admin bilan bo'lanishni iloji yo'q")
    elif message.text == "📍 Bizning manzil":
        if data["location"]:
            longitude = data['location']["longitude"]
            latitude = data['location']['latitude']
            bot.send_location(message.chat.id, latitude, longitude)
        else:
            bot.send_message(message.chat.id, "Uzur hali mazilimiz yo'q")
    else:
        data['users'][message.chat.id]["name_enterprise"] = new_name
        bot.send_message(message.chat.id, user_my_profile_create(message), reply_markup=keyboard_user_my_profile())


@bot.callback_query_handler(func=lambda x: x.data == "name_enterprise")
def name_enterprise(call):
    name = data["users"][call.message.chat.id]["name_enterprise"]
    if name == "-":
        bot.edit_message_text(
            "Korxonani nomini kiriting",
            call.message.chat.id,
            call.message.id,
            reply_markup=keyboard_user_back_my_profile()
        )
        bot.register_next_step_handler(call.message, update_name_enterprise)
    else:
        bot.edit_message_text(
            f"Sizning korxona nomi: {name}\n"
            f"Korxonani nomini kiriting",
            call.message.chat.id,
            call.message.id,
            reply_markup=keyboard_user_back_my_profile()
        )
        bot.register_next_step_handler(call.message, update_name_enterprise)


"""----------------- user  tugilgan kun qator --------------------"""


def update_birthday(message):
    if message.text == "🔖 Tadbirlar":
        text = "Muvoffaqiyat tajriba natijasi\n" \
               "Tajriba-mag'lubiyatlar natojasi\n\n" \
               "Har bosib o'tilgan yol, o'z izini qoldiradi"
        bot.send_message(message.chat.id, text, reply_markup=keyboard_user_event())
    elif message.text == "👤 Mening profilim":
        bot.send_message(message.chat.id, user_my_profile_create(message), reply_markup=keyboard_user_my_profile())
    elif message.text == "📞 Admin bilan bog'lanish":
        if data["phone"]:
            text = ""
            for s in data["phone"]:
                text += s + "\n"
            bot.send_message(message.chat.id, text, reply_markup=get_keyboard_link())
        else:
            bot.send_message(message.chat.id, "Uzur hozircha admin bilan bo'lanishni iloji yo'q")
    elif message.text == "📍 Bizning manzil":
        if data["location"]:
            longitude = data['location']["longitude"]
            latitude = data['location']['latitude']
            bot.send_location(message.chat.id, latitude, longitude)
        else:
            bot.send_message(message.chat.id, "Uzur hali mazilimiz yo'q")
    else:
        date = message.text.split(".")
        day = date[0]
        moth = date[1]
        year = date[2]
        if moth[0] == "0":
            moth = moth[1]
        if day.isdigit() and year.isdigit() and moth.isdigit():
            if (1935 < int(year) < 2015) and (1<=int(moth)<=12) and (1 <= int(day) <= 31):
                data['users'][message.chat.id]["birthday"] = message.text
                bot.send_message(message.chat.id, user_my_profile_create(message), reply_markup=keyboard_user_my_profile())

            else:
                bot.send_message(message.chat.id, "Sizning tug'ilgan kuningiz qabul qilinmadi")
        else:
            bot.send_message(message.chat.id, "Sizning tug'ilgan kuningiz qabul qilinmadi\n"
                                              "Iltimos tug'ilgan kuningizni boshqatdan kiriting",
                             reply_markup=keyboard_user_back_my_profile())
            bot.register_next_step_handler(message, update_birthday)


@bot.callback_query_handler(func=lambda x: x.data == "birthday")
def birthday(call):
    bot.edit_message_text(
        "Tug'ilgan kunningizni kirting.\n"
        "(kun.oy.yil)\n"
        "Masalan: 10.05.1999",
        call.message.chat.id,
        call.message.id,
        reply_markup=keyboard_user_back_my_profile()
    )
    bot.register_next_step_handler(call.message, update_birthday)


"""------------- user favoliya turi qatori --------------------------"""


@bot.callback_query_handler(func=lambda x: "type_activity_" in x.data)
def update_type_activity(call):
    new_type_activity = call.data.split("_")[-1].capitalize()
    data['users'][call.message.chat.id]["type_activity"] = new_type_activity
    bot.edit_message_text(
@bot.callback_query_handler(func=lambda x: x.data == "birthday")
def birthday(call):
    bot.edit_message_text(
        "Tug'ilgan kunningizni kirting.\n"
        "(kun.oy.yil)\n"
        "Masalan: 10.05.1999",
        call.message.chat.id,
        call.message.id,
        reply_markup=keyboard_user_back_my_profile()
    )
    bot.register_next_step_handler(call.message, update_birthday)

        user_my_profile_create(call.message),
        call.message.chat.id,
        call.message.id,
        reply_markup=keyboard_user_my_profile()
    )



@bot.callback_query_handler(func=lambda x: x.data == "type_activity")
def type_activity(call):
    bot.edit_message_text(
        "🔹 Qaysi sohada faoliyat yuritasiz? 👇",
        call.message.chat.id,
        call.message.id,
        reply_markup=type_activity_keyboard()
    )


def type_activity_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("Ishlab chiqarish", callback_data="type_activity_ishlab chiqarish")
    btn2 = InlineKeyboardButton("Xizmat ko'rsatish", callback_data="type_activity_xizmat ko'rsatish")
    btn3 = InlineKeyboardButton("Savdo sotiq", callback_data="type_activity_savdo sotiq")
    btn4 = InlineKeyboardButton("Ta'lim", callback_data="type_activity_ta'lim")
    btn5 = InlineKeyboardButton("Boshqalar", callback_data="type_activity_boshqalar")
    btn6 = InlineKeyboardButton("Vaqtincha ishsiz", callback_data="type_activity_vaqtincha ishsiz")
    return keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6)


"""---------- user viloya talash qatori -----------------------------------"""


@bot.callback_query_handler(func=lambda x: "region_" in x.data and len(x.data.split("_")) == 3)
def choose_region(call):
    choose = call.data.split("_")[1:]
    user_id = call.message.chat.id
    if choose[1] != "res":
        data["users"][user_id]["region"] = f"{choose[0].capitalize()} {choose[1]}"
    else:
        data["users"][user_id]["region"] = f"{choose[0].capitalize()} {choose[1].capitalize()}"
    bot.edit_message_text(
        user_my_profile_create(call.message),
        call.message.chat.id,
        call.message.id,
        reply_markup=keyboard_user_my_profile()
    )



@bot.callback_query_handler(func=lambda x: x.data == "region")
def region_call(call):
    bot.edit_message_text(
        "✅ Qaysi viloyatdansiz 👇",
        call.message.chat.id,
        call.message.id,
        reply_markup=keyboard_region()
    )


def keyboard_region():
    keyboard = InlineKeyboardMarkup(row_width=2)
    toshkent = InlineKeyboardButton("Toshkent shahar", callback_data="region_toshkent_shahar")
    toshkent_v = InlineKeyboardButton("Toshkent viloyati", callback_data="region_toshkent_viloyati")
    andijon_v = InlineKeyboardButton("Andijon viloyati", callback_data="region_andijon_viloyati")
    buxoro_v = InlineKeyboardButton("Buxoro viloyati", callback_data="region_buxoro_viloyati")
    jizzax_v = InlineKeyboardButton("Jizzax viloyati", callback_data="region_jizzax_viloyati")
    qashqadaryo_v = InlineKeyboardButton("Qashqadaryo viloyati", callback_data="region_qashqadaryo_viloyati")
    navoiy_v = InlineKeyboardButton("Navoiy viloyati", callback_data="region_navoiy_viloyati")
    namangan_v = InlineKeyboardButton("Namangan ciloyati", callback_data="region_namanga_viloyati")
    samarqand_v = InlineKeyboardButton("Samarqand viloyati", callback_data="region_samarqand_viloyati")
    surxandaryo_v = InlineKeyboardButton("Surxandaryo viloyati", callback_data="region_surxandaryo_viloyati")
    sirdaryo_v = InlineKeyboardButton("Sirdaryo viloyati", callback_data="region_sirdaryo_viloyati")
    fargona_v = InlineKeyboardButton("Farg'ona viloyati", callback_data="region_farg'ona_viloyati")
    xorazm_v = InlineKeyboardButton("Xorazm viloyati", callback_data="region_xorazm_viloyati")
    qoraqalpogiston_r = InlineKeyboardButton("Qoraqalpog'iston Res", callback_data="region_qoraqalpog'iston_res")
    keyboard.add(toshkent, toshkent_v, andijon_v, buxoro_v, jizzax_v, qashqadaryo_v)
    keyboard.add(navoiy_v, namangan_v, samarqand_v, surxandaryo_v, sirdaryo_v, fargona_v)
    keyboard.add(xorazm_v, qoraqalpogiston_r)
    return keyboard


"""--------------------- user telefon nomer o'zgartirish ----------------------------"""


def user_mobile_number_update(message):
    new_phone = message.text
    if new_phone.startswith("+998") and len(new_phone) == 13 and new_phone[1:].isdigit():
        data['users'][message.chat.id]['mobile_number'] = new_phone
        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)
        bot.send_message(message.chat.id, user_my_profile_create(message), reply_markup=keyboard_user_my_profile())
    elif message.text == "🔖 Tadbirlar":
        text = "Muvoffaqiyat tajriba natijasi\n" \
               "Tajriba-mag'lubiyatlar natojasi\n\n" \
               "Har bosib o'tilgan yol, o'z izini qoldiradi"
        bot.send_message(message.chat.id, text, reply_markup=keyboard_user_event())
    elif message.text == "👤 Mening profilim":
        bot.send_message(message.chat.id, user_my_profile_create(message), reply_markup=keyboard_user_my_profile())
    elif message.text == "📞 Admin bilan bog'lanish":
        if data["phone"]:
            text = ""
            for s in data["phone"]:
                text += s + "\n"
            bot.send_message(message.chat.id, text, reply_markup=get_keyboard_link())
        else:
            bot.send_message(message.chat.id, "Uzur hozircha admin bilan bo'lanishni iloji yo'q")
    elif message.text == "📍 Bizning manzil":
        if data["location"]:
            longitude = data['location']["longitude"]
            latitude = data['location']['latitude']
            bot.send_location(message.chat.id, latitude, longitude)
        else:
            bot.send_message(message.chat.id, "Uzur hali mazilimiz yo'q")
    else:
        bot.send_message(message.chat.id,
                         "Sizning Telefon raqam qabul qilinmadi\n"
                         "Iltimos Telefon raqamni boshqatdan kiriting",
                         reply_markup=keyboard_user_back_my_profile())
        bot.register_next_step_handler(message, user_mobile_number_update)


@bot.callback_query_handler(func=lambda x: x.data == "mobile_number")
def user_mobile_number_update_call(call):
    if data['users'][call.message.chat.id]["mobile_number"] == "-":
        bot.edit_message_text(
            "Yangi telefon nomer kiriting",
            call.message.chat.id,
            call.message.id,
            reply_markup=keyboard_user_back_my_profile()
        )
        bot.register_next_step_handler(call.message, user_mobile_number_update)
    else:
        user_phone = data['users'][call.message.chat.id]["mobile_number"]
        bot.edit_message_text(
            f"Sizning Telefon raqam: {user_phone}\n"
            f"Yangilash uchun Telefon raqam kiriting",
            call.message.chat.id,
            call.message.id
        )
        bot.register_next_step_handler(call.message, user_mobile_number_update)


"""---------- user ism familiyasini ozgartiradi -------------"""


def update_user_name(message):
    type_name = data["type"][message.chat.id]
    new_name = message.text
    type = {
        "first_name": "Ism",
        "last_name": "Familiya"
    }
    if new_name.isalpha() and detection(message) :
        data['users'][message.chat.id][type_name] = new_name.capitalize()
        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)
        bot.send_message(message.chat.id, user_my_profile_create(message), reply_markup=keyboard_user_my_profile())
    elif message.text == "🔖 Tadbirlar":
        text = "Muvoffaqiyat tajriba natijasi\n" \
               "Tajriba-mag'lubiyatlar natojasi\n\n" \
               "Har bosib o'tilgan yol, o'z izini qoldiradi"
        bot.send_message(message.chat.id, text, reply_markup=keyboard_user_event())
    elif message.text == "👤 Mening profilim":
        bot.send_message(message.chat.id, user_my_profile_create(message), reply_markup=keyboard_user_my_profile())
    elif message.text == "📞 Admin bilan bog'lanish":
        if data["phone"]:
            text = ""
            for s in data["phone"]:
                text += s + "\n"
            bot.send_message(message.chat.id, text, reply_markup=get_keyboard_link())
        else:
            bot.send_message(message.chat.id, "Uzur hozircha admin bilan bo'lanishni iloji yo'q")
    elif message.text == "📍 Bizning manzil":
        if data["location"]:
            longitude = data['location']["longitude"]
            latitude = data['location']['latitude']
            bot.send_location(message.chat.id, latitude, longitude)
        else:
            bot.send_message(message.chat.id, "Uzur hali mazilimiz yo'q")
    else:
        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)
        bot.send_message(message.chat.id, f"Sizning {type[type_name]} qabul qilinmadi\n"
                                          f"Iltimos ismni boshqatdan kiriting", reply_markup=keyboard_user_back_my_profile())
        bot.register_next_step_handler(message, update_user_name)


@bot.callback_query_handler(func=lambda x: x.data.split("_")[1] == "name")
def user_name_call(call):
    type_name = call.data
    data['type'][call.message.chat.id] = type_name
    type = {
        "first_name": "Ism",
        "last_name": "Familiya"
    }
    user_name = data["users"][call.message.chat.id][type_name]
    bot.edit_message_text(
        f"Sizning {type[type_name]} {user_name}\n"
        f"Yangililash uchun yangi {type[type_name]} kiriting",
        call.message.chat.id,
        call.message.id,
        reply_markup=keyboard_user_back_my_profile()
    )
    bot.register_next_step_handler(call.message, update_user_name)

"""----------user mening profilimni menyga qaytish --------------------"""


@bot.callback_query_handler(func=lambda x: x.data == "back_user_my_profile")
def back_user_my_profile(call):
    bot.edit_message_text(
        user_my_profile_create(call.message),
        call.message.chat.id,
        call.message.id,
        reply_markup=keyboard_user_my_profile()
    )


def keyboard_user_back_my_profile():
    keyboard = InlineKeyboardMarkup()
    btn = InlineKeyboardButton("Ortga", callback_data="back_user_my_profile")
    return keyboard.add(btn)


"----------keybaord user my profile ------------------------"


def keyboard_user_my_profile():
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("Ism 📝", callback_data="first_name")
    btn2 = InlineKeyboardButton("Familiya 📝", callback_data="last_name")
    btn4 = InlineKeyboardButton("Telefon raqam 📝", callback_data="mobile_number")
    btn5 = InlineKeyboardButton("Viloyat 📝", callback_data="region")
    btn6 = InlineKeyboardButton("Favoliyat turi 📝", callback_data="type_activity")
    btn7 = InlineKeyboardButton("Korxona nomi 📝", callback_data="name_enterprise")
    btn8 = InlineKeyboardButton("Lavozim 📝", callback_data="position")
    btn9 = InlineKeyboardButton("Tugilgan kun 📝", callback_data="birthday")
    return keyboard.add(btn4, btn1, btn2, btn5, btn6, btn7, btn8, btn9)


"------------------user my profile create -----------------------"


def icons(first_name, last_name, mobile_number, region, type_activity, position, birthday, enterprise):
    d = (first_name, last_name, mobile_number, region, type_activity, position, birthday, enterprise)
    l = []
    for s in d:
        if s == "-":
            l += ["❗️"]
        else:
            l += ["✅"]
    return l


def user_my_profile_create(message):
    if message.chat.id not in data['users']:
        first_name = message.from_user.first_name
        if message.from_user.last_name:
            last_name = message.from_user.last_name
            mobile_number = region = type_activity = position = enterprise = birthday = "-"
        else:
            last_name = mobile_number = region = type_activity = position = enterprise = birthday = "-"
        data['users'][message.chat.id] = {
            "first_name": first_name,
            "last_name": last_name,
            "mobile_number": mobile_number,
            "region": region,
            "type_activity": type_activity,
            "position": position,
            "birthday": birthday,
            "name_enterprise": enterprise,
            "user_event": []
        }
    else:
        first_name = data['users'][message.chat.id]['first_name']
        last_name = data["users"][message.chat.id]['last_name']
        mobile_number = data['users'][message.chat.id]['mobile_number']
        region = data['users'][message.chat.id]["region"]
        type_activity = data['users'][message.chat.id]["type_activity"]
        position = data['users'][message.chat.id]["position"]
        birthday = data['users'][message.chat.id]['birthday']
        enterprise = data["users"][message.chat.id]["name_enterprise"]

    icon = icons(first_name, last_name, mobile_number, region, type_activity, position, birthday, enterprise)

    text = f"{icon[0]}Ism: {first_name}\n" \
           f"{icon[1]}Familiya: {last_name}\n" \
           f"{icon[2]}Telfon nomer: {mobile_number}\n" \
           f"{icon[3]}Viloyat: {region}\n" \
           f"{icon[4]}Favoliyat turi: {type_activity}\n" \
           f"{icon[7]}Korxona nomi: {enterprise}\n" \
           f"{icon[5]}Lavozim: {position}\n" \
           f"{icon[6]}Tug'ilgan kun: {birthday}"

    return text


def keyboard_user_my_profile():
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("Ism 📝", callback_data="first_name")
    btn2 = InlineKeyboardButton("Familiya 📝", callback_data="last_name")
    btn4 = InlineKeyboardButton("Telefon raqam 📝", callback_data="mobile_number")
    btn5 = InlineKeyboardButton("Viloyat 📝", callback_data="region")
    btn6 = InlineKeyboardButton("Favoliyat turi 📝", callback_data="type_activity")
    btn7 = InlineKeyboardButton("Korxona nomi 📝", callback_data="name_enterprise")
    btn8 = InlineKeyboardButton("Lavozim 📝", callback_data="position")
    btn9 = InlineKeyboardButton("Tugilgan kun 📝", callback_data="birthday")
    return keyboard.add(btn4, btn1, btn2, btn5, btn6, btn7, btn8, btn9)


"----------------user table event regiration  -------------------------"


def user_event_table(message):
    if message.chat.id in data['users']:
        if data['users'][message.chat.id]['user_event']:
            user_events = (data['users'][message.chat.id]['user_event'])
            text = ""
            new_table = []
            for s in user_events:
                if s in data['event']:
                    new_table += [s]
                    text += f"{data['event'][s][0]}\n\n"
            return text
        else:
            return "Tadbir mavjud emas"
    else:
        return "Tadbir mavjud emas"


@bot.callback_query_handler(func=lambda x: x.data == "user_registration_table")
def user_registration_table(call):
    bot.edit_message_text(
        user_event_table(call.message),
        call.message.chat.id,
        call.message.id,
        reply_markup=keyboard_user_back_event()
    )


"----------------- user registration event -------------------------------------"


@bot.callback_query_handler(func=lambda x: x.data == "salom")
def salom(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.send_message(call.message.chat.id, event(), reply_markup=keyboard_user_next_event())


def validate(dct):
    for s in dct.values():
        if s == "-":
            return False
    return True


@bot.callback_query_handler(func=lambda x: x.data == "event_choose")
def user_event_choose(call):
    user_id = call.message.chat.id
    if user_id not in data['users']:
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(
            call.message.chat.id,
            "Iltimos malumotlarizni to'lidiring"
        )

    else:
        user_data = data['users'][call.message.chat.id]
        user_validate = validate(user_data)
        if user_validate:
            number = data["user_event"][call.message.chat.id]
            user_event = data["users"][call.message.chat.id]["user_event"]
            data["users"][call.message.chat.id]["user_event"] = user_event + [number]
            text = data["event"][int(number)][0]
            photo = data["event"][int(number)][1]
            bot.delete_message(call.message.chat.id, call.message.id)

            if number not in data['user_event']:
                data['user_event'][number] = [call.message.chat.id]
            else:
                sum = data['user_event'][number]
                data['user_event'][number] = sum + [call.message.chat.id]

            bot.send_message(call.message.chat.id, f"Siz {text[:15]}... tadbirga ro'yxatdan otdingiz")
            data["user_event"][call.message.chat.id] = 0
        else:
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(
                call.message.chat.id,
                "Iltimos malumotlarizni to'lidiring",
            )


def keyboard_user_event_choose():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("Ro'yxatdan o'tish", callback_data="event_choose")
    btn2 = InlineKeyboardButton("Ortga", callback_data="salom")
    return keyboard.add(btn1, btn2)


@bot.callback_query_handler(func=lambda x: "next_event_" in x.data)
def next_event_registration(call):
    number = call.data.split("_")[-1]
    data["user_event"][call.message.chat.id] = number
    photo = data['event'][int(number)][1]
    text = f"{number}) {data['event'][int(number)][0]}"
    data["photo_id"] = call.message.chat.id
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.send_photo(call.message.chat.id, photo, text, reply_markup=keyboard_user_event_choose())


@bot.callback_query_handler(func=lambda x: x.data == "back__user__event")
def back__admin__event__call(call):
    text = "Muvoffaqiyat tajriba natijasi\n" \
           "Tajriba-mag'lubiyatlar natojasi\n\n" \
           "Har bosib o'tilgan yol, o'z izini qoldiradi"
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.id,
        reply_markup=keyboard_user_event()
    )


def keyboard_user_next_event():
    keyboard = InlineKeyboardMarkup()
    for s in data['event']:
        text = data["event"][s][0]
        keyboard.add(
            InlineKeyboardButton(f"{s}) {text[:15]}...", callback_data=f"next_event_{s}")
        )
    keyboard.add(InlineKeyboardButton("Ortga", callback_data="back__user__event"))
    return keyboard


@bot.callback_query_handler(func=lambda x: x.data == "user_next_event")
def next_event_call(call):
    bot.edit_message_text(
        event(),
        call.message.chat.id,
        call.message.id,
        reply_markup=keyboard_user_next_event()
    )


"-------------------------------------------keyboard----------------------------------------"


def keyboard_user_event():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("Navbatdagi tadbirlar", callback_data="user_next_event")
    btn2 = InlineKeyboardButton("Ro'yxatdan o'tilgan tadbirlar", callback_data="user_registration_table")
    keyboard.add(btn1, btn2)
    return keyboard


@bot.callback_query_handler(func=lambda x: x.data == "user_back_event")
def user_back_event(call):
            text = "Muvoffaqiyat tajriba natijasi\n" \
                   "Tajriba-mag'lubiyatlar natojasi\n\n" \
                   "Har bosib o'tilgan yol, o'z izini qoldiradi"
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.id,
                reply_markup=keyboard_user_event()
            )


def keyboard_user_back_event():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton('Ortga', callback_data="user_back_event")
    )


"--------------admin event user registration table---------------------------"


def get_keyboard_admin_back_event_registration():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Ortga", callback_data="get_admin_event_table")
    )


@bot.callback_query_handler(func=lambda x: "admin_table_event_registration_" in x.data)
def admin_table_event_registration(call):
    number = int(call.data.split("_")[-1])
    text = ""
    for user_id in data['users']:
        if number in data['users'][user_id]["user_event"]:
            first_name = data['users'][user_id]["first_name"]
            last_name = data['users'][user_id]["last_name"]
            mobile_number = data["users"][user_id]['mobile_number']
            text += f"{first_name} {last_name} {mobile_number} \n"
    if text == "":
        text = "Ro'yxatdan o'tkan odam yo'q"
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.id,
        reply_markup=get_keyboard_admin_back_event_registration()
    )


@bot.callback_query_handler(func=lambda x: x.data == "admin_back_event")
def admin_back_event(call):
    bot.edit_message_text(
        event(),
        call.message.chat.id,
        call.message.id,
        reply_markup=keyboard_admin_event_meny()
    )


def keyboard_admin_event_table():
    keyboard = InlineKeyboardMarkup()
    for s in data['event']:
        keyboard.add(
            InlineKeyboardButton(f"{s}", callback_data=f"admin_table_event_registration_{s}")
        )
    return keyboard.add(
        InlineKeyboardButton("Ortga", callback_data="admin_back_event")
    )


@bot.callback_query_handler(func=lambda x: x.data == "get_admin_event_table")
def admin_table_user_registration(call):
    bot.edit_message_text(
        event(),
        call.message.chat.id,
        call.message.id,
        reply_markup=keyboard_admin_event_table()
    )


"----------------- admin delete event ----------------------------"


@bot.callback_query_handler(func=lambda x: "delete_event_" in x.data)
def delete_event_in_table_call(call):
    number = int(call.data.split("_")[-1])
    new_table = {}
    for s in data['event']:
        if s != number:
            new_table[s] = data["event"][s]
    data['event'] = new_table
    bot.edit_message_text(
        "Tadbir o'chirildi",
        call.message.chat.id,
        call.message.id
    )


def keyboard_admin_delete_event_table():
    keyboard = InlineKeyboardMarkup()
    for s in data['event']:
        text = data["event"][s][0]
        keyboard.add(
            InlineKeyboardButton(f"{s}) {text[:15]}...", callback_data=f"delete_event_{s}")
        )
    keyboard.add(InlineKeyboardButton("Ortga", callback_data="admin_back_event_meny"))
    return keyboard


@bot.callback_query_handler(func=lambda x: x.data == "admin_delete_event")
def admin_delete_event_call(call):
    bot.edit_message_text(
        event(),
        call.message.chat.id,
        call.message.id,
        reply_markup=keyboard_admin_delete_event_table()
    )


"------------------- admin add event ------------------"


def admin_create_event_photo(message):
    if message.photo:
        photo = message.photo[-1].file_id
        number = data["event_sum"] - 1
        text = data["event"][number]
        data["event"][number] = text + [photo]
        bot.send_message(message.chat.id, "Tadbirga rasm qabul qilindi")
    elif message.text and message.text == "Tadbirlar":
        number = data["event_sum"] - 1
        data["event"].pop(number)
        data['event_sum'] = number
        bot.send_message(message.chat.id, event(), reply_markup=keyboard_admin_event_meny())
    elif message.text and message.text == "Manzil":
        number = data["event_sum"] - 1
        data["event"].pop(number)
        data['event_sum'] = number
        bot.send_message(message.chat.id, "Yengi manzil kiriting")
        bot.register_next_step_handler(message, create_location)
    elif message.text and message.text == "Telefon nomer":
        number = data["event_sum"] - 1
        data["event"].pop(number)
        data['event_sum'] = number
        bot.send_message(message.chat.id, "Iltimos malumot kiriting")
        bot.register_next_step_handler(message, create)
    elif message.text and message.text == "Admin":
        number = data["event_sum"] - 1
        data["event"].pop(number)
        data['event_sum'] = number
        bot.send_message(message.chat.id, "Iltimos qo'shmoqchi bo'lgan admindan bitta habarni forward qiling")
        bot.register_next_step_handler(message, add_new_admin)
    else:
        number = data["event_sum"] - 1
        data["event"].pop(number)
        data['event_sum'] = number
        bot.send_message(message.chat.id, "Iltimos rasm kiring"),
        bot.register_next_step_handler(message, admin_create_event_photo)


def admin_create_event_name(message):
    if message.text and detection(message):
        number = data['event_sum']
        data['event'][number] = [message.text]
        data["event_sum"] = number + 1
        bot.send_message(message.chat.id, "Matn qo'shildi\nEndi rasm kiriting")
        bot.register_next_step_handler(message, admin_create_event_photo)
    elif message.text and message.text == "Tadbirlar":
        bot.send_message(message.chat.id, event(), reply_markup=keyboard_admin_event_meny())
    elif message.text and message.text == "Manzil":
        bot.send_message(message.chat.id, "Yengi manzil kiriting")
        bot.register_next_step_handler(message, create_location)
    elif message.text and message.text == "Telefon nomer":
        bot.send_message(message.chat.id, "Iltimos malumot kiriting")
        bot.register_next_step_handler(message, create)
    elif message.text and message.text == "Admin":
        bot.send_message(message.chat.id, "Iltimos qo'shmoqchi bo'lgan admindan bitta habarni forward qiling")
        bot.register_next_step_handler(message, add_new_admin)
    else:
        bot.send_message(message.chat.id, "Iltimos matn kiriting")
        bot.register_next_step_handler(message, admin_create_event_name)


@bot.callback_query_handler(func=lambda x: x.data == "admin_add_event")
def admin_add_event_call(call):
    bot.edit_message_text(
        "Tadbir matnni kiriting",
        call.message.chat.id,
        call.message.id,
        reply_markup=keyboard_admin_back_event_meny()
    )
    bot.register_next_step_handler(call.message, admin_create_event_name)


def event():
    table = data['event']
    if table:
        text = ""
        for s in table:
            text += f"{s}) " + data["event"][s][0] + '\n'
        return text
    return "Tadbir yo'q"


@bot.callback_query_handler(func=lambda x: x.data == "admin_back_event_meny")
def admin_back_event_meny_call(call):
    bot.edit_message_text(
        event(),
        call.message.chat.id,
        call.message.id,
        reply_markup=keyboard_admin_event_meny()
    )


def keyboard_admin_back_event_meny():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Ortga", callback_data="admin_back_event_meny")
    )


def keyboard_admin_event_meny():
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("Qoshish", callback_data="admin_add_event")
    btn2 = InlineKeyboardButton("O'chirish", callback_data="admin_delete_event")
    btn3 = InlineKeyboardButton("Ro'yxatdan otkanlarni ro'yxati", callback_data="get_admin_event_table")
    return keyboard.add(btn1, btn2, btn3)


"""-------------- admin location qo'shadigan qator -----------------------------"""


def create_location(message):
    if message.location:
        longitude = message.location.longitude
        latitude = message.location.latitude
        data["location"]["longitude"] = longitude
        data["location"]["latitude"] = latitude
        bot.send_message(message.chat.id, "Manzil o'zgartirildi")
    elif message.text == "Tadbirlar":
        bot.send_message(message.chat.id, event(), reply_markup=keyboard_admin_event_meny())


    elif message.text == "Manzil":
        pass
    elif message.text == "Admin":
        pass
    elif message.text == "Telefon nomer":
        pass


"--------------------------link  ------------------------------"


def get_keyboard_link():
    keyboard = InlineKeyboardMarkup(row_width=3)
    tg = InlineKeyboardButton("Telegram", url="https://t.me/infact")
    tel = InlineKeyboardButton("Telefon", url="https://link-to-tel.herokuapp.com/tel/%2B998903332442")
    insta = InlineKeyboardButton("Instagram", url="https://www.instagram.com/infact.uz/")
    return keyboard.add(tg, tel, insta)


"----------------------- start and text --------------------------"


def detection(message):
    admin_text = ["Tadbirlar", "Manzil", "Telefon nomer", "Admin"]
    user_text = ["🔖 Tadbirlar", "📍 Bizning manzil", "📞 Admin bilan bog'lanish", "👤 Mening profilim"]
    if message.text in admin_text or message.text in user_text:
        return False
    return True


def meny_keyboard(message):
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn0 = KeyboardButton("Tadbirlar")
    btn1 = KeyboardButton("🔖 Tadbirlar")
    btn2 = KeyboardButton("Manzil")
    btn3 = KeyboardButton("📍 Bizning manzil")
    btn4 = KeyboardButton("📞 Admin bilan bog'lanish")
    btn5 = KeyboardButton("Telefon nomer")
    btn6 = KeyboardButton("Admin")
    btn7 = KeyboardButton("👤 Mening profilim")

    if message.chat.id in data["admin"]:
        keyboard.add(btn0, btn2, btn5, btn6)
    else:
        keyboard.add(btn1, btn3, btn7, btn4)

    return keyboard


@bot.message_handler(func=lambda x: x.text == "📍 Bizning manzil")
def bizning_mazil(message):
    if data["location"]:
        longitude = data['location']["longitude"]
        latitude = data['location']['latitude']
        bot.send_location(message.chat.id, latitude, longitude)
    else:
        bot.send_message(message.chat.id, "Uzur hali mazilimiz yo'q")


@bot.message_handler(func=lambda x: x.text == "Manzil")
def manzil(message):
    bot.send_message(message.chat.id, "Yengi manzil kiriting")
    bot.register_next_step_handler(message, create_location)


@bot.message_handler(func=lambda x: "Tadbirlar" in x.text)
def tadbirlar(message):
    if message.chat.id in data['admin']:
        bot.send_message(message.chat.id, event(), reply_markup=keyboard_admin_event_meny())
    else:
        text = "Muvoffaqiyat tajriba natijasi\n" \
               "Tajriba-mag'lubiyatlar natojasi\n\n" \
               "Har bosib o'tilgan yol, o'z izini qoldiradi"
        bot.send_message(message.chat.id, text, reply_markup=keyboard_user_event())


@bot.message_handler(func=lambda x: x.text == "👤 Mening profilim")
def mening_profilim(message):
    bot.send_message(message.chat.id, user_my_profile_create(message), reply_markup=keyboard_user_my_profile())


@bot.message_handler(func=lambda x: x.text == "📞 Admin bilan bog'lanish")
def admin_bilan_boglanish(message):
    if data["phone"]:
        text = ""
        for s in data["phone"]:
            text += s + "\n"
        bot.send_message(message.chat.id, text, reply_markup=get_keyboard_link())
    else:
        bot.send_message(message.chat.id, "Uzur hozircha admin bilan bo'lanishni iloji yo'q")


@bot.message_handler(func=lambda x: x.text == "Admin")
def admin_(message):
    bot.send_message(message.chat.id, "Iltimos qo'shmoqchi bo'lgan admindan bitta habarni forward qiling")
    bot.register_next_step_handler(message, add_new_admin)


@bot.message_handler(func=lambda x: x.text == "Telefon nomer")
def telefon_nomer(message):
    bot.send_message(message.chat.id, "Iltimos malumot kiriting")
    bot.register_next_step_handler(message, create)

@bot.message_handler(commands="start")
def send_welcome(message):
    keyboard = meny_keyboard(message)
    bot.send_message(message.chat.id, f"Xush kelib siz {message.from_user.first_name}", reply_markup=keyboard)


bot.polling(non_stop=True)
