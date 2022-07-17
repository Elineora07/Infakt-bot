def register_text(user_id, data):
    first_name = data['user'][user_id]['first_name']
    last_name = data['user'][user_id]['last_name']
    middle_name = data['user'][user_id]['middle_name']
    phone = data['user'][user_id]['phone']
    text = f"Ism: {first_name}\n" \
           f"Familiya: {last_name}\n" \
           f"Sharif: {middle_name}\n" \
           f"Telefon raqam: {phone}"

    return text
