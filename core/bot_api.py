from telebot import types, TeleBot

from config import API_TOKEN
from database import db_app
from database.models import TgUser, Doc

bot = TeleBot(API_TOKEN)


@bot.message_handler(func=lambda message: message.text == 'Початок')
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if TgUser.query.filter_by(chat_id=message.chat.id).first() is None:
        user = TgUser(chat_id=message.chat.id)
        db_app.session.add(user)
        db_app.session.commit()
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Підписатись на розсилання')
    itembtn2 = types.KeyboardButton('Показники лічильників')
    markup.add(itembtn1, itembtn2)
    bot.reply_to(message, "Добрий день! Вітаємо вас", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Показники лічильників')
def counter(message):
    if TgUser.query.filter_by(chat_id=message.chat.id).first() is None:
        bot.send_message(message.chat.id, "Помилка!")
        return
    bot.send_message(message.chat.id,
                     f"""
\t*[Електрика](https://www.energy.mk.ua/)*
\t*[Вода](https://www.vodokanal.mk.ua/)*
\t*[Газ](https://ok.104.ua/ua/signin)*""",
                     parse_mode='MarkdownV2')


@bot.message_handler(func=lambda message: message.text == 'Підписатись на розсилання')
def enable_subscribe(message):
    user = TgUser.query.filter_by(chat_id=message.chat.id).first()
    if user is None:
        markup = types.ReplyKeyboardMarkup()
        markup.add(types.KeyboardButton('Початок'))
        bot.reply_to(message, 'Помилка!', reply_markup=markup)
    if user.enabled:
        markup = types.ReplyKeyboardMarkup()
        itembtn1 = types.KeyboardButton('Відписатись від розсилання')
        itembtn2 = types.KeyboardButton('Показники лічильників')
        markup.add(itembtn1, itembtn2)
        bot.reply_to(message, "Ви вже підписані на розсилку", reply_markup=markup)
        return
    user.enabled = True
    db_app.session.commit()
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('Відписатись від розсилання')
    itembtn2 = types.KeyboardButton('Показники лічильників')
    markup.add(itembtn1, itembtn2)
    bot.reply_to(message, "Тепер ви будете отримувати розсилку щодо аварійних відключень", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Відписатись від розсилання')
def disable_subscribe(message):
    user = TgUser.query.filter_by(chat_id=message.chat.id).first()
    if user is None:
        markup = types.ReplyKeyboardMarkup()
        markup.add(types.KeyboardButton('Початок'))
        bot.reply_to(message, 'Помилка!', reply_markup=markup)
    if not user.enabled:
        markup = types.ReplyKeyboardMarkup()
        itembtn1 = types.KeyboardButton('Підписатись на розсилання')
        itembtn2 = types.KeyboardButton('Показники лічильників')
        markup.add(itembtn1, itembtn2)
        bot.reply_to(message, "Ви ще не підписались на розсилку", reply_markup=markup)
        return
    user.enabled = False
    db_app.session.commit()
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('Підписатись на розсилання')
    itembtn2 = types.KeyboardButton('Показники лічильників')
    markup.add(itembtn1, itembtn2)
    bot.reply_to(message, "Ви усіпшно відписались від розсилки щодо відключень", reply_markup=markup)


@bot.message_handler(commands=['start_send'])
def disable_subscribe(message):
    doc = Doc.query.first()
    users = TgUser.query.filter_by(enabled=True).all()
    for user in users:
        bot.send_message(user.chat_id, doc.content)
