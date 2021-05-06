from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

from app import app

db = SQLAlchemy(app)

Session = sessionmaker()
Session.configure(bind=db.engine)
session = Session()
