from .database import db_app


class TgUser(db_app.Model):
    id = db_app.Column(db_app.BigInteger, primary_key=True)
    chat_id = db_app.Column(db_app.Integer)

    def __repr__(self):
        return f'<TgUser {self.id}, {self.chat_id}>'
