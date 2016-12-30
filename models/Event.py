from application import db
from datetime import date

User_Event = db.Table('User_Event',
                      db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
                      db.Column('event_id', db.Integer, db.ForeignKey('Event.id')),
                      db.Column('result', db.Integer)
                      )


class Event(db.Model):
    __tablename__ = "Event"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256))
    startDate = db.Column(db.DateTime)
    endDate = db.Column(db.DateTime)
    local = db.Column(db.String(256))

    # Many to Many
    acceptedGuests = db.relationship('User', secondary=User_Event)
    # One to Many
    rejectedInvitations = db.relationship('User')
    # One to Many
    pendingInvitations = db.relationship('User')
    # Many to Many


    description = db.Column("description", db.String(256))
    price = db.Column("price", db.Integer)
    host = db.Column("host", db.ForeignKey('User.id'))

    def __init__(self, id, title, startDate, endDate, local, acceptedGuests,
                 rejectedInvitations, pendingInvitations, description, price, owner):
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
        self.host = owner
