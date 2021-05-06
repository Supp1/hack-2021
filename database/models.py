class TgUser(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    chat_id = db.Column(db.Integer)

    def __repr__(self):
        return f'<TgUser {self.id}, {self.chat_id}>'

