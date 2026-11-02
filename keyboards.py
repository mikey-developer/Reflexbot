from telebot import types


def gender_keyboard(lang):

    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    if lang == "uz":
        keyboard.add("Erkak", "Ayol")
    else:
        keyboard.add("Мужчина", "Женщина")

    return keyboard


def education_keyboard(lang):

    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    if lang == "uz":
        keyboard.add("O'rta", "O'rta maxsus")
        keyboard.add("Oliy", "Tugallanmagan oliy")
    else:
        keyboard.add("Среднее", "Среднее специальное")
        keyboard.add("Высшее", "Неоконченное высшее")

    return keyboard


def family_keyboard(lang):

    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    if lang == "uz":
        keyboard.add("Uylanmagan / Turmushga chiqmagan")
        keyboard.add("Uylangan / Turmushga chiqqan")
        keyboard.add("Ajrashgan")
    else:
        keyboard.add("Не женат / Не замужем")
        keyboard.add("Женат / Замужем")
        keyboard.add("Разведён / Разведена")

    return keyboard


def phone_keyboard(lang):

    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    if lang == "uz":
        button = types.KeyboardButton(
            "📱 Raqamni yuborish",
            request_contact=True
        )
    else:
        button = types.KeyboardButton(
            "📱 Отправить номер",
            request_contact=True
        )

    keyboard.add(button)

    return keyboard


def confirm_keyboard(lang):

    keyboard = types.InlineKeyboardMarkup()

    if lang == "uz":
        send = types.InlineKeyboardButton(
            "📨 Yuborish",
            callback_data="send_application"
        )

        cancel = types.InlineKeyboardButton(
            "❌ Bekor qilish",
            callback_data="cancel_application"
        )
    else:
        send = types.InlineKeyboardButton(
            "📨 Отправить",
            callback_data="send_application"
        )

        cancel = types.InlineKeyboardButton(
            "❌ Отменить",
            callback_data="cancel_application"
        )

    keyboard.add(send)
    keyboard.add(cancel)

    return keyboard