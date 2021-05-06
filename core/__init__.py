from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/db/highliter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

from core import app_api, bot_api
