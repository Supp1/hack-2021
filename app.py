import time

from sqlalchemy import create_engine

from config import WEBHOOK_URL_BASE, WEBHOOK_URL_PATH
from core import app
from core.bot_api import bot
from database import db_app

if __name__ == '__main__':
    # bot.remove_webhook()
    #
    # time.sleep(0.1)
    # Set webhook
    # bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
    db_app.init_app(app)
    with app.app_context():
        eng = db_app.engine
        db_app.create_engine('sqlite:///static/db/hacka.db')

