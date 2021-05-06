import time

from telebot import types, TeleBot

API_TOKEN = ''

WEBHOOK_URL_BASE = "https://9b7f536ebbf9.ngrok.io"
WEBHOOK_URL_PATH = "/%s" % API_TOKEN

bot = TeleBot(API_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # inlineKeyboard = types.InlineKeyboardMarkup()
    # item1 = types.InlineKeyboardButton("", callback_data='enable')
    # item2 = types.InlineKeyboardButton("", callback_data='counter')
    # inlineKeyboard.add(item1, item2)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Підписатись на розсилання')
    itembtn2 = types.KeyboardButton('Показники лічильників')
    markup.add(itembtn1, itembtn2)
    bot.reply_to(message, "Hi, i am PublicServiceBot", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Показники лічильників')
def counter(message):
    if TgUser.query.filter_by(chat_id=message.chat.id).first() is None:
        bot.send_message(message.chat.id, "Помилка!")
        return
    bot.send_message(message.chat.id, "У прогресі розробки")


@bot.callback_query_handler(func=lambda call: call.data == 'enable')
# @bot.message_handler(commands=['enable'])
def enable_subscribe(message):
    if TgUser.query.filter_by(chat_id=message.chat.id).first() is not None:
        bot.send_message(message.chat.id, "Ви вже підписані на розсилку")
        return
    user = TgUser(chat_id=message.chat.id)
    db.session.add(user)
    db.session.commit()
    bot.send_message(message.chat.id, "Тепер ви будете отримувати розсилку щодо аварійних відключень")


@bot.message_handler(commands=['disable'])
def disable_subscribe(message):
    if TgUser.query.filter_by(chat_id=message.chat.id).first() is None:
        bot.send_message(message.chat.id, "Ви ще не підписались")
        return
    TgUser.query.filter(TgUser.chat_id == message.chat.id).delete()
    db.session.commit()
    bot.send_message(message.chat.id, "Ви відписались від розсилки")


#
#
#
# def send_planned_turnoff():
#     users = TgUser.query.all()
#     clip = HighlightClip.query.order_by(HighlightClip.id.desc()).first()
#     for user in users:
#         bot.send_message(user.chat_id, clip.url)
#
#
# def send_emegrency_turnoff(name):
#     users = TgUser.query.all()
#     for user in users:
#         bot.send_video(user.chat_id, )

# @app.route('/save_urls', methods=['POST'])
# def save_url():
#     request_body_dict = request.json
#     clip_url = request_body_dict['url']
#     clip = HighlightClip(url=clip_url, state=False)
#     db.session.add(clip)
#     db.session.commit()
#     send_clips_url()
#     return app.response_class(
#         response='OK',
#         status=200,
#         mimetype='core/json'
#     )
#
bot.remove_webhook()

time.sleep(0.1)

# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
