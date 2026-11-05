import telebot
from telebot import types
from config import ADMIN_ID
from config import TOKEN
from texts import TEXTS
from states import QUESTIONS
from keyboards import (
    gender_keyboard,
    education_keyboard,
    family_keyboard,
    phone_keyboard,
    confirm_keyboard
)

bot = telebot.TeleBot(TOKEN)

def send_application(user_id):

    user = users[user_id]
    answers = user["answers"]
    lang = user["lang"]

    text = "📩 YANGI ARIZA\n\n"

    for question in QUESTIONS:

        if question == "photo":
            continue

        value = answers.get(question, "-")

        text += f"{TEXTS[lang][question]}\n"
        text += f"{value}\n\n"

   
    keyboard = types.InlineKeyboardMarkup()

    checked = types.InlineKeyboardButton(
        "✅ Tekshirildi",
        callback_data=f"checked_{user_id}"
    )

    keyboard.add(checked)

    
    bot.send_message(
        ADMIN_ID,
        text,
        reply_markup=keyboard
    )

   
    photo = answers.get("photo")

    if photo:
        bot.send_photo(
            ADMIN_ID,
            photo,
            caption=f"📷 Nomzod selfisi: {answers['fio']}"
        )

    bot.send_message(
        user_id,
        TEXTS[lang]["done"],
        reply_markup=types.ReplyKeyboardRemove()
    )

    del users[user_id]

# Foydalanuvchilar ma'lumotlari
users = {}

@bot.callback_query_handler(func=lambda call: call.data == "send_application")
def confirm_send(call):

    user_id = call.from_user.id

    if user_id not in users:
        bot.answer_callback_query(
            call.id,
            "Ariza topilmadi!"
        )
        return

    send_application(user_id)

    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "cancel_application")
def cancel_application(call):

    user_id = call.from_user.id

    if user_id in users:

        lang = users[user_id]["lang"]

        del users[user_id]

        bot.edit_message_text(
            TEXTS[lang]["cancelled"],
            call.message.chat.id,
            call.message.message_id
        )

    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("checked_"))
def application_checked(call):

    user_id = call.from_user.id

    if user_id != ADMIN_ID:
        bot.answer_callback_query(
            call.id,
            "Sizda ruxsat yo'q!",
            show_alert=True
        )
        return

    bot.edit_message_text(
        f"{call.message.text}\n\n✅ Обработан",
        call.message.chat.id,
        call.message.message_id
    )

    bot.answer_callback_query(
        call.id,
        "Ariza tekshirildi!"
    )

@bot.message_handler(commands=['start'])
def start(message):

    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            "🇺🇿 O'zbekcha",
            callback_data="lang_uz"
        ),
        types.InlineKeyboardButton(
            "🇷🇺 Русский",
            callback_data="lang_ru"
        )
    )

    bot.send_message(
        message.chat.id,
        "Tilni tanlang / Выберите язык:",
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("lang_"))
def select_language(call):

    lang = call.data.split("_")[1]
    user_id = call.from_user.id

    users[user_id] = {
        "lang": lang,
        "step": 0,
        "answers": {}
    }

    bot.answer_callback_query(call.id)

    bot.edit_message_text(
        "Til tanlandi." if lang == "uz" else "Язык выбран."
        ,
        call.message.chat.id,
        call.message.message_id
    )

    ask_question(user_id)

def ask_question(user_id):

    user = users[user_id]
    lang = user["lang"]
    step = user["step"]

    question = QUESTIONS[step]
    text = TEXTS[lang][question]

    if question == "gender":
        bot.send_message(
            user_id,
            text,
            reply_markup=gender_keyboard(lang)
        )

    elif question == "education":
        bot.send_message(
            user_id,
            text,
            reply_markup=education_keyboard(lang)
        )

    elif question == "family":
        bot.send_message(
            user_id,
            text,
            reply_markup=family_keyboard(lang)
        )

    elif question == "phone":
        bot.send_message(
            user_id,
            text,
            reply_markup=phone_keyboard(lang)
        )

    else:
        bot.send_message(
            user_id,
            text,
            reply_markup=types.ReplyKeyboardRemove()
        )


@bot.message_handler(content_types=['text', 'photo', 'contact'])
def get_answer(message):

    user_id = message.from_user.id

    if user_id not in users:
        return

    user = users[user_id]

    step = user["step"]
    question = QUESTIONS[step]

    # Selfi
    if question == "photo":

        if message.photo:
            user["answers"]["photo"] = message.photo[-1].file_id

        else:
            user["answers"]["photo"] = None

    # Telefon
    elif question == "phone":

        if message.contact:
            user["answers"]["phone"] = message.contact.phone_number

        else:
            user["answers"]["phone"] = message.text

    # Oddiy matn
    else:

        if not message.text:
            return

        user["answers"][question] = message.text

    user["step"] += 1

    # Barcha savollar tugadi
    if user["step"] >= len(QUESTIONS):

        show_confirmation(user_id)

    else:

        ask_question(user_id)

def show_confirmation(user_id):

    user = users[user_id]
    lang = user["lang"]
    answers = user["answers"]

    text = TEXTS[lang]["confirm"] + "\n\n"

    for question in QUESTIONS:

        value = answers.get(question)

        if question == "photo":
            value = "Yuborildi 📷" if value else "Yuborilmadi"

        text += f"• {TEXTS[lang][question]}\n"
        text += f"{value}\n\n"

    bot.send_message(
        user_id,
        text,
        reply_markup=confirm_keyboard(lang)
    )


bot.infinity_polling()