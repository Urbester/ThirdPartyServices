from application import db


class User(db.Model):
    __tablename__ = "User"

    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    email = db.Column("email", db.String(256), unique=True)
    name = db.Column("name", db.String(256))
    accessToken = db.Column("accessToken", db.String(256))
    photoLink = db.Column("photoLink", db.String(256))

    def __init__(self, name, accessToken, email, photoLink):
        self.name = name
        self.email = email
        self.accessToken = accessToken
        self.photoLink = photoLink
