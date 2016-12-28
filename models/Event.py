from application import db
from datetime import date


class Event(db.Model):
    __tablename__ = "Event"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256))
    startDate = db.Column(db.DateTime)
    endDate = db.Column(db.DateTime)
    local = db.Column(db.String(256))
    # One to Many
    acceptedGuests = db.relationship('User')
    # One to Many
    rejectedInvitations = db.relationship('User')
    # One to Many
    pendingInvitations = db.relationship('User')
    description = db.Column(db.String(256))
    price = db.Column(db.Integer)
    owner = db.Column(db.relationship('User'))

    def __init__(self, id, title, startDate, endDate, local, acceptedGuests,
                 rejectedInvitations, pendingInvitations, description, price, owner, accessToken):
        self.id = id
        self.title = title
        self.startDate = startDate
        self.endDate = endDate
        self.local = local
        self.acceptedGuests = acceptedGuests
        self.rejectedInvitations = rejectedInvitations
        self.pendingInvitations = pendingInvitations
        self.description = description
        self.price = price
        self.owner = owner
