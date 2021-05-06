import logging

from flask import Flask
from flask_crontab import Crontab

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../static/db/hacka2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.logger.setLevel(logging.ERROR)
crontab = Crontab(app)

from core import app_api, bot_api
