import time

from config import *
from core import app
from core.bot_api import bot
from database import db_app

if __name__ == '__main__':
    bot.remove_webhook()

    time.sleep(1)
    # Set webhook
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
    db_app.init_app(app)
    db_app.create_all()
    app.run(debug=True)
