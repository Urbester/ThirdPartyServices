from application import db


class User(db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256))
    accessToken = db.Column(db.String(256))

    def __init__(self, email, accessToken):
        self.email = email
        self.accessToken = accessToken
