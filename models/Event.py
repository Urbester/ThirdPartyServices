from application import db

class Event(db.Model):
    __tablename__ = "Event"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256))
    # One to Many Example
    acceptedGuests = db.relationship('User')


    def __init__(self, title, acceptedGuests):
        self.title = title
        self.acceptedGuests = acceptedGuests
