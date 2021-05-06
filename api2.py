import time

import telebot
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

API_TOKEN = 'none'

# WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_BASE = "https://9b7f536ebbf9.ngrok.io"
WEBHOOK_URL_PATH = "/%s" % API_TOKEN

bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/db/hacka.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

Session = sessionmaker()
Session.configure(bind=db.engine)
session = Session()


class TgUser(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    chat_id = db.Column(db.Integer)

    def __repr__(self):
        return f'<TgUser {self.id}, {self.chat_id}>'


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@app.route('/<token>', methods=['POST'])
def handle(token):
    if token == bot.token:
        request_body_dict = request.json
        update = telebot.types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return app.response_class(
            response='OK',
            status=200,
            mimetype='application/json'
        )
    else:
        return app.response_class(
            response='Error',
            status=403,
            mimetype='application/json'
        )


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hi, i am PublicServiceBot")


@bot.message_handler(commands=['enable'])
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
#         mimetype='application/json'
#     )
#
bot.remove_webhook()

time.sleep(0.1)

# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

if __name__ == '__main__':
    app.run(debug=True)
    db.create_all()
