from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

from app import app

db_app = SQLAlchemy(app)

Session = sessionmaker()
Session.configure(bind=db_app.engine)
session = Session()
