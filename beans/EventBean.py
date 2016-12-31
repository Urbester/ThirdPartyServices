class EventBean(object):
    def new_event(self, title, startDate, endDate, local, description, price, owner, public, maxGuests, URL):
        try:
            from models import Event
            from models import User
            from application import db
            if URL == "":
                event = Event(title=title, startDate=startDate, endDate=endDate,
                              local=local, description=description, price=price, owner=owner, public=public, maxGuests=maxGuests)
            else:
                event = Event(title=title, startDate=startDate, endDate=endDate,
                              local=local, description=description, price=price, owner=owner, public=public, maxGuests=maxGuests, URL=URL)
            db.session.add(event)
            db.session.commit()
            self.result = "Event created."
            return True
        except Exception as event:
            self.result = "Error creating event."
            return False

    # NICE TO HAVE, NOT TESTED
    def update_event(self, id, title, startDate, endDate, local,
                     description, price, owner):
        try:
            from models import Event
            from application import db
            event = Event.query.filter_by(id=id, owner=owner).first()
            event.title = title
            event.startDate = startDate
            event.endDate = endDate
            event.local = local
            event.description = description
            event.price = price
            db.session.commit()
            self.result = "Event updated"
            return True
        except Exception as exception:
            self.result = "Update Error"
            return False

    def delete_event(self, id, host):
        try:
            from models import Event
            from application import db
            event = Event.query.filter_by(id=int(id), host=host.id).first()
            db.session.delete(event)
            db.session.commit()
            self.result = "Event was deleted."
            return True
        except Exception as exception:
            self.result = "Event doesn't exist."
            return False

    def get_event(self, id):
        try:
            from models import Event, User
            event = Event.query.filter_by(id=id).first()
            accepted_users = Event.query.filter_by(id=id).first().accepted
            host_user = User.query.filter_by(id=event.host).first()
            self.result = {
                "id": event.id,
                "title": event.title,
                "startDate": event.startDate.strftime("%Y-%m-%d %H:%M:%S"),
                "endDate": event.endDate.strftime("%Y-%m-%d %H:%M:%S"),
                "local": event.local,
                "description": event.description,
                "price": event.price,
                "host_name": host_user.name,
                "host_email": host_user.email,
                "host_URL": host_user.photoLink,
                "maxGuests": event.maxGuests,
                "slotsLeft": event.maxGuests - len(accepted_users),
                "URL": event.URL
            }
            return True
        except Exception as exception:
            self.result = "Event doesn't exist."
            return False

    def accept_event(self, event_id, user):
        try:
            from models import User, Event
            from application import db
            event = Event.query.filter_by(id=event_id).first()
            event.accepted.append(user)
            try:
                event.invited.remove(user)
            except Exception as e:
                try:
                    event.pending.remove(user)
                except:
                    self.result = "ERROR"

            db.session.commit()
            self.result = "Accepted Event"
            return True
        except Exception as exception:
            self.result = "ERROR"
            return False

    def reject_event(self, event_id, user):
        try:
            from models import User, Event
            from application import db
            event = Event.query.filter_by(id=event_id).first()
            event.rejected.append(user)
            db.session.commit()
            self.result = "Rejected Event"
            return True
        except Exception as exception:
            self.result = "ERROR"
            return False

    def invite_users(self, invite_list, event_id, owner):
        try:
            from models import User, Event
            from application import db
            event = Event.query.filter_by(id=event_id, host=owner.id).first()
            for i in invite_list:
                if User.query.filter_by(email=i).first() is not None:
                    event.invited.append(User.query.filter_by(email=i).first())
            db.session.commit()
            self.result = "Invited User"
            return True
        except Exception as exception:
            self.result = "ERROR"
            return False

    def reject_user_from_event(self, invite_list, event_id, owner):
        try:
            from models import User, Event
            from application import db
            event = Event.query.filter_by(id=event_id, host=owner.id).first()
            for i in invite_list:
                if User.query.filter_by(email=invite_list[i]).first() is not None:
                    event.rejected.append(User.query.filter_by(email=invite_list[i]).first())
            db.session.commit()
            self.result = "Rejected User"
            return True
        except Exception as exception:
            self.result = "ERROR"
            return False

    def ask_to_join_event(self, event_id, owner):
        try:
            from models import User, Event
            from application import db
            event = Event.query.filter_by(id=event_id, isPublic=True).first()
            event.pending.append(User.query.filter_by(email=owner.email).first())
            db.session.commit()
            self.result = "Asked to event"
            return True
        except Exception as exception:
            self.result = "ERROR"
            return False

    def get_event_list(self, user):
        try:
            from models import Event, User
            event_set = Event.query.filter(Event.isPublic == True, Event.host != user.id)
            event_list = []
            for event in event_set:
                host_user = User.query.filter_by(id=event.host).first()
                accepted_users = Event.query.filter_by(id=event.id).first().accepted
                event_list.append({
                    "id": event.id,
                    "title": event.title,
                    "startDate": event.startDate.strftime("%Y-%m-%d %H:%M:%S"),
                    "endDate": event.endDate.strftime("%Y-%m-%d %H:%M:%S"),
                    "local": event.local,
                    "description": event.description,
                    "price": event.price,
                    "host_name": host_user.name,
                    "host_email": host_user.email,
                    "host_URL": host_user.photoLink,
                    "maxGuests": event.maxGuests,
                    "slotsLeft": event.maxGuests - len(accepted_users),
                    "URL": event.URL
                })
            self.result = event_list
            return True
        except Exception as exception:
            self.result = "Event doesn't exist."
            return False

    def get_hosting_event_list(self, user):
        try:
            from models import Event, User
            event_set = Event.query.filter_by(host=user.id)
            event_list = []
            for event in event_set:
                accepted_users = Event.query.filter_by(id=event.id).first().accepted
                event_list.append({
                    "id": event.id,
                    "title": event.title,
                    "startDate": event.startDate.strftime("%Y-%m-%d %H:%M:%S"),
                    "endDate": event.endDate.strftime("%Y-%m-%d %H:%M:%S"),
                    "local": event.local,
                    "description": event.description,
                    "price": event.price,
                    "host_name": user.name,
                    "host_email": user.email,
                    "host_URL": user.photoLink,
                    "maxGuests": event.maxGuests,
                    "slotsLeft": event.maxGuests - len(accepted_users),
                    "URL": event.URL
                })
            self.result = event_list
            return True
        except Exception as exception:
            self.result = "Event doesn't exist."
            return False

    def get_accepted_event_list(self, user):
        try:
            from models import Event, User
            event_set = User.query.filter_by(id=user.id).first().accepted
            event_list = []
            for event in event_set:
                accepted_users = Event.query.filter_by(id=event.id).first().accepted
                event_list.append({
                    "id": event.id,
                    "title": event.title,
                    "startDate": event.startDate.strftime("%Y-%m-%d %H:%M:%S"),
                    "endDate": event.endDate.strftime("%Y-%m-%d %H:%M:%S"),
                    "local": event.local,
                    "description": event.description,
                    "price": event.price,
                    "host_name": user.name,
                    "host_email": user.email,
                    "host_URL": user.photoLink,
                    "maxGuests": event.maxGuests,
                    "slotsLeft": event.maxGuests - len(accepted_users),
                    "URL": event.URL
                })
            self.result = event_list
            return True
        except Exception as exception:
            self.result = "Event doesn't exist."
            return False

    def get_rejected_event_list(self, user):
        try:
            from models import Event, User
            event_set = User.query.filter_by(id=user.id).first().rejected
            event_list = []
            for event in event_set:
                accepted_users = Event.query.filter_by(id=event.id).first().accepted
                event_list.append({
                    "id": event.id,
                    "title": event.title,
                    "startDate": event.startDate.strftime("%Y-%m-%d %H:%M:%S"),
                    "endDate": event.endDate.strftime("%Y-%m-%d %H:%M:%S"),
                    "local": event.local,
                    "description": event.description,
                    "price": event.price,
                    "host_name": user.name,
                    "host_email": user.email,
                    "host_URL": user.photoLink,
                    "maxGuests": event.maxGuests,
                    "slotsLeft": event.maxGuests - len(accepted_users),
                    "URL": event.URL
                })
            self.result = event_list
            return True
        except Exception as exception:
            self.result = "Event doesn't exist."
            return False

    def get_pending_event_list(self, user):
        try:
            from models import Event, User
            event_set = User.query.filter_by(id=user.id).first().pending
            event_list = []
            for event in event_set:
                accepted_users = Event.query.filter_by(id=event.id).first().accepted
                event_list.append({
                    "id": event.id,
                    "title": event.title,
                    "startDate": event.startDate.strftime("%Y-%m-%d %H:%M:%S"),
                    "endDate": event.endDate.strftime("%Y-%m-%d %H:%M:%S"),
                    "local": event.local,
                    "description": event.description,
                    "price": event.price,
                    "host_name": user.name,
                    "host_email": user.email,
                    "host_URL": user.photoLink,
                    "maxGuests": event.maxGuests,
                    "slotsLeft": event.maxGuests - len(accepted_users),
                    "URL": event.URL
                })
            self.result = event_list
            return True
        except Exception as exception:
            self.result = "Event doesn't exist."
            return False

    def get_invited_event_list(self, user):
        try:
            from models import Event, User
            event_set = User.query.filter_by(id=user.id).first().invited
            event_list = []
            for event in event_set:
                accepted_users = Event.query.filter_by(id=event.id).first().accepted
                event_list.append({
                    "id": event.id,
                    "title": event.title,
                    "startDate": event.startDate.strftime("%Y-%m-%d %H:%M:%S"),
                    "endDate": event.endDate.strftime("%Y-%m-%d %H:%M:%S"),
                    "local": event.local,
                    "description": event.description,
                    "price": event.price,
                    "host_name": user.name,
                    "host_email": user.email,
                    "host_URL": user.photoLink,
                    "maxGuests": event.maxGuests,
                    "slotsLeft": event.maxGuests - len(accepted_users),
                    "URL": event.URL
                })
            self.result = event_list
            return True
        except Exception as exception:
            self.result = "Event doesn't exist."
            return False
