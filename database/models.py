from .database import db_app


class TgUser(db_app.Model):
    id = db_app.Column(db_app.Integer, autoincrement=True, primary_key=True)
    chat_id = db_app.Column(db_app.Integer)
    enabled = db_app.Column(db_app.Boolean, default=False)

    def __repr__(self):
        return f'<TgUser {self.id}, {self.chat_id}>'


class Doc(db_app.Model):
    id = db_app.Column(db_app.Integer, autoincrement=True, primary_key=True)
    content = db_app.Column(db_app.VARCHAR(1024))
