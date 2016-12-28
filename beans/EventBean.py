class EventBean(object):
    def new_event(self, title, startDate, endDate, local, description, price, owner, accessToken):
        try:
            from models import Event
            from models import User
            from application import db
            event = Event(title=title, startDate=startDate, endDate=endDate,
                          local=local, description=description, price=price,owner=owner)
            db.session.add(event)
            db.session.commit()
            self.result = "Event created."
            return True
        except Exception as event:
            self.result = "Error creating event."
            return False

    def update_event(self, id, title, startDate, endDate, local,
                      description, price, owner):
        try:
            from models import Event
            from application import db
            event = Event.query.filter_by(id=self.id,owner=owner).first()
            event.title = title
            event.startDate = startDate
            event.endDate = endDate
            event.local = local
            event.description = description
            event.price = price
            db.session.commit()
            self.result = "Event updated"
        except Exception as exception:
            self.result = "Update Error"
            return False

    def delete_event(self, id, owner):
        try:
            from models import Event
            from application import db
            event = Event.query.filter_by(id=self.id,owner=owner).first()
            db.session.delete(event)
            db.session.commit()
            self.result = "Event was deleted."
            return True
        except Exception as exception:
            self.result = "Event doesn't exist."
            return False

    def get_event(self, id):
        try:
            from models import Event
            event = Event.query.filter_by(id=self.id).first()
            self.result = {"title": event.title, "startDate": event.startDate, "endDate": event.endDate,
                           "local": event.local, "acceptedGuests": event.acceptedGuests,
                           "rejectedInvitations": event.rejectedInvitations,
                           "pendingInvitations": event.pendingInvitations,
                           "description": event.description, "price": event.price, "owner": event.owner}
            return True
        except Exception as exception:
            self.result = "Event doesn't exist."
            return False
