from application import db
from datetime import date

User_InvitedTo_Event = db.Table('Invited_Event',
                                db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
                                db.Column('event_id', db.Integer, db.ForeignKey('Event.id')),
                                )

User_Accepted_Event = db.Table('Accepted_Event',
                               db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
                               db.Column('event_id', db.Integer, db.ForeignKey('Event.id')),
                               )

User_Rejected_Event = db.Table('Rejected_Event',
                               db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
                               db.Column('event_id', db.Integer, db.ForeignKey('Event.id')),
                               )

User_Pending_Event = db.Table('Pending_Event',
                              db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
                              db.Column('event_id', db.Integer, db.ForeignKey('Event.id')),
                              )


class Event(db.Model):
    __tablename__ = "Event"

    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    title = db.Column("title", db.String(256))
    startDate = db.Column("startDate", db.DateTime)
    endDate = db.Column("endDate", db.DateTime)
    local = db.Column("local", db.String(256))
    description = db.Column("description", db.String(256))
    price = db.Column("price", db.Integer)
    host = db.Column("host", db.ForeignKey('User.id'))
    isPublic = db.Column("isPublic", db.Boolean, default=False)
    URL = db.Column("URL", db.String(512), default="http://lorempixel.com/400/200/nightlife/")

    # Relations
    accepted = db.relationship("User", secondary=User_Accepted_Event,
                               backref=db.backref('accepted_event', lazy='dynamic'))
    rejected = db.relationship("User", secondary=User_Rejected_Event,
                               backref=db.backref('rejected_event', lazy='dynamic'))
    invited = db.relationship("User", secondary=User_InvitedTo_Event,
                              backref=db.backref('invited_event', lazy='dynamic'))
    pending = db.relationship("User", secondary=User_Pending_Event, backref=db.backref('pending_event', lazy='dynamic'))

    def __init__(self, title, startDate, endDate, local, description, price, owner, public, URL=None):
        self.title = title
        self.startDate = startDate
        self.endDate = endDate
        self.local = local
        self.description = description
        self.price = price
        self.isPublic = public
        self.host = owner
        self.URL = URL
