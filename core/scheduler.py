from core import crontab
from core.bot_api import bot
from database import TgUser, Doc


@crontab.job(minute="30", hour="0")
def my_scheduled_job():
    doc = Doc.query.first()
    users = TgUser.query.filter_by(enabled=True).all()
    for user in users:
        bot.send_message(user.chat_id, doc.content, parse_mode='MarkdownV2')
