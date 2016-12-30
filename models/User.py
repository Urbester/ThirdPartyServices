from application import db
from models import User_Accepted_Event
from models import User_InvitedTo_Event
from models import User_Pending_Event
from models import User_Rejected_Event


class User(db.Model):
    __tablename__ = "User"

    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    email = db.Column("email", db.String(256), unique=True)
    name = db.Column("name", db.String(256))
    accessToken = db.Column("accessToken", db.String(256))
    photoLink = db.Column("photoLink", db.String(256))
    pending = db.relationship("Event", secondary=User_Pending_Event, backref=db.backref('pending_user', lazy='dynamic'))
    accepted = db.relationship("Event", secondary=User_Accepted_Event, backref=db.backref('accepted_accepted', lazy='dynamic'))
    rejected = db.relationship("Event", secondary=User_Rejected_Event, backref=db.backref('rejected_user', lazy='dynamic'))
    invited = db.relationship("Event", secondary=User_InvitedTo_Event, backref=db.backref('invited_user', lazy='dynamic'))

    def __init__(self, name, accessToken, email, photoLink):
        self.name = name
        self.email = email
        self.accessToken = accessToken
        self.photoLink = photoLink
