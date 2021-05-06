from flask import request
from telebot import types

from app import app
from core.bot_api import bot
from database.models import TgUser


@app.route('/test', methods=['GET'])
def test():
    TgUser.query.get(1)
    print('helloworld')
    return app.response_class(
        response='OK',
        status=200,
        mimetype='core/json'
    )


@app.route('/<token>', methods=['POST'])
def handle(token):
    if token == bot.token:
        request_body_dict = request.json
        update = types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return app.response_class(
            response='OK',
            status=200,
            mimetype='core/json'
        )
    else:
        return app.response_class(
            response='Error',
            status=403,
            mimetype='core/json'
        )
