class EventBean(object):
    def new_event(self, title, startDate, endDate, local, description, price, owner, public, maxGuests, URL):  #
        try:
            from models import Event
            from models import User
            from application import db
            if URL == "":
                event = Event(title=title, startDate=startDate, endDate=endDate,
                              local=local, description=description, price=price, owner=owner, public=public,
                              maxGuests=maxGuests)
            else:
                event = Event(title=title, startDate=startDate, endDate=endDate,
                              local=local, description=description, price=price, owner=owner, public=public,
                              maxGuests=maxGuests, URL=URL)
            db.session.add(event)
            db.session.commit()
            self.result = "Event created."
            return True
        except Exception as event:
            self.result = "Error creating event."
            return False

    # NICE TO HAVE, NOT TESTED
    def update_event(self, id, title, startDate, endDate, local, description, price, owner):  #
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

    def delete_event(self, id, host):  #
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

    def get_event(self, id, token):  #
        try:
            from models import Event, User, User_Accepted_Event, User_Rejected_Event, User_InvitedTo_Event, \
                User_Pending_Event

            event = Event.query.filter_by(id=id).first()
            user = User.query.filter_by(accessToken=token).first()

            isHosting = "false"
            isAccepted = "false"
            isPending = "false"
            isRejected = "false"
            isInvited = "false"

            # check if is hosting the event
            host_user = User.query.filter_by(id=event.host).first()
            if host_user.accessToken == token:
                isHosting = "true"

            # check if is in accepted list of event
            accepted_users = Event.query.filter_by(id=id).first().accepted
            if user in accepted_users:
                isAccepted = "true"

            # check if is pending list of event
            pending_users = Event.query.filter_by(id=id).first().pending
            if user in pending_users:
                isPending = "true"

            # check if is in rejected list of event
            rejected = Event.query.filter_by(id=id).first().rejected
            if len(rejected) > 0:
                isRejected = "true"

            # check if is invited list of event
            invited = Event.query.filter_by(id=id).first().invited
            if user in invited:
                isInvited = "true"

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
                "isHosting": isHosting,
                "isPending": isPending,
                "isInvited": isInvited,
                "isRejected": isRejected,
                "isAccepted": isAccepted,
                "slotsLeft": event.maxGuests - len(accepted_users),
                "URL": event.URL
            }
            return True
        except Exception as exception:
            self.result = "Event doesn't exist."
            return False

    def accept_event(self, event_id, user):  #
        try:
            from models import User, Event
            from application import db
            event = Event.query.filter_by(id=event_id).first()
            event.accepted.append(user)
            event.invited.remove(user)
            db.session.commit()
            self.result = "Accepted Event"
            return True
        except Exception as exception:
            self.result = "ERROR"
            return False

    def reject_event(self, event_id, user):  #
        try:
            from models import User, Event
            from application import db
            event = Event.query.filter_by(id=event_id).first()
            event.invited.remove(user)
            event.rejected.append(user)
            db.session.commit()
            self.result = "Rejected Event"
            return True
        except Exception as exception:
            self.result = "ERROR"
            return False

    def invite_users(self, user_email, event_id, owner):  #
        try:
            from models import User, Event
            from application import db
            event = Event.query.filter_by(id=event_id, host=owner.id).first()
            event.invited.append(User.query.filter_by(email=user_email).first())
            db.session.commit()
            self.result = "Invited User"
            return True
        except Exception as exception:
            self.result = "ERROR"
            return False

    def accept_pending(self, user_email, event_id, owner):  #
        try:
            from models import User, Event
            from application import db
            event = Event.query.filter_by(id=event_id, host=owner.id).first()
            user = User.query.filter_by(email=user_email).first()
            event.pending.remove(user)
            event.accepted.append(user)
            db.session.commit()
            self.result = "User accepted"
            return True
        except Exception as e:
            self.result = "ERROR accepting user, check if owner"
            return False

    def reject_pending(self, user_email, event_id, owner):  #
        try:
            from models import User, Event
            from application import db
            event = Event.query.filter_by(id=event_id, host=owner.id).first()
            user = User.query.filter_by(email=user_email).first()
            event.pending.remove(user)
            event.rejected.append(user)
            db.session.commit()
            self.result = "User accepted"
            return True
        except Exception as e:
            self.result = "ERROR accepting user, check if owner"
            return False

    def ask_to_join_event(self, event_id, owner):  #
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

    def get_event_list(self, user):  #
        try:
            from models import Event, User
            event_set = Event.query.filter(Event.isPublic == True, Event.host != user.id)
            event_list = []
            for event in event_set:

                isHosting = "false"
                isAccepted = "false"
                isPending = "false"
                isRejected = "false"
                isInvited = "false"

                # check if is hosting the event
                host_user = User.query.filter_by(id=event.host).first()
                if host_user.accessToken == user.accessToken:
                    isHosting = "true"

                # check if is in accepted list of event
                accepted_users = Event.query.filter_by(id=event.id).first().accepted
                if user in accepted_users:
                    isAccepted = "true"

                # check if is pending list of event
                pending_users = Event.query.filter_by(id=event.id).first().pending
                if user in pending_users:
                    isPending = "true"

                # check if is in rejected list of event
                rejected = Event.query.filter_by(id=event.id).first().rejected
                if user in rejected:
                    isRejected = "true"

                # check if is invited list of event
                invited = Event.query.filter_by(id=event.id).first().invited
                if user in invited:
                    isInvited = "true"

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
                    "isHosting": isHosting,
                    "isPending": isPending,
                    "isInvited": isInvited,
                    "isRejected": isRejected,
                    "isAccepted": isAccepted,
                    "slotsLeft": event.maxGuests - len(accepted_users),
                    "URL": event.URL
                })
            self.result = event_list
            return True
        except Exception as exception:
            self.result = "Event doesn't exist."
            return False

    def get_hosting_event_list(self, user):  #
        try:
            from models import Event, User
            event_set = Event.query.filter_by(host=user.id)
            event_list = []
            for event in event_set:
                isHosting = "false"
                isAccepted = "false"
                isPending = "false"
                isRejected = "false"
                isInvited = "false"

                # check if is hosting the event
                host_user = User.query.filter_by(id=event.host).first()
                if host_user.accessToken == user.accessToken:
                    isHosting = "true"

                # check if is in accepted list of event
                accepted_users = Event.query.filter_by(id=event.id).first().accepted
                if user in accepted_users:
                    isAccepted = "true"

                # check if is pending list of event
                pending_users = Event.query.filter_by(id=event.id).first().pending
                if user in pending_users:
                    isPending = "true"

                # check if is in rejected list of event
                rejected = Event.query.filter_by(id=event.id).first().rejected
                if user in rejected:
                    isRejected = "true"

                # check if is invited list of event
                invited = Event.query.filter_by(id=event.id).first().invited
                if user in invited:
                    isInvited = "true"

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
                    "isHosting": isHosting,
                    "isPending": isPending,
                    "isInvited": isInvited,
                    "isRejected": isRejected,
                    "isAccepted": isAccepted,
                    "slotsLeft": event.maxGuests - len(accepted_users),
                    "URL": event.URL
                })
            self.result = event_list
            return True
        except Exception as exception:
            self.result = "Event doesn't exist."
            return False

    def get_accepted_event_list(self, user):  #
        try:
            from models import Event, User
            event_set = User.query.filter_by(id=user.id).first().accepted
            event_list = []
            for event in event_set:

                isHosting = "false"
                isAccepted = "false"
                isPending = "false"
                isRejected = "false"
                isInvited = "false"

                # check if is hosting the event
                host_user = User.query.filter_by(id=event.host).first()
                if host_user.accessToken == user.accessToken:
                    isHosting = "true"

                # check if is in accepted list of event
                accepted_users = Event.query.filter_by(id=event.id).first().accepted
                if user in accepted_users:
                    isAccepted = "true"

                # check if is pending list of event
                pending_users = Event.query.filter_by(id=event.id).first().pending
                if user in pending_users:
                    isPending = "true"

                # check if is in rejected list of event
                rejected = Event.query.filter_by(id=event.id).first().rejected
                if user in rejected:
                    isRejected = "true"

                # check if is invited list of event
                invited = Event.query.filter_by(id=event.id).first().invited
                if user in invited:
                    isInvited = "true"

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
                    "isHosting": isHosting,
                    "isPending": isPending,
                    "isInvited": isInvited,
                    "isRejected": isRejected,
                    "isAccepted": isAccepted,
                    "slotsLeft": event.maxGuests - len(accepted_users),
                    "URL": event.URL
                })
            self.result = event_list
            return True
        except Exception as exception:
            self.result = "Event doesn't exist."
            return False

    def get_rejected_event_list(self, user):  #
        try:
            from models import Event, User
            event_set = User.query.filter_by(id=user.id).first().rejected
            event_list = []
            for event in event_set:
                isHosting = "false"
                isAccepted = "false"
                isPending = "false"
                isRejected = "false"
                isInvited = "false"

                # check if is hosting the event
                host_user = User.query.filter_by(id=event.host).first()
                if host_user.accessToken == user.accessToken:
                    isHosting = "true"

                # check if is in accepted list of event
                accepted_users = Event.query.filter_by(id=event.id).first().accepted
                if user in accepted_users:
                    isAccepted = "true"

                # check if is pending list of event
                pending_users = Event.query.filter_by(id=event.id).first().pending
                if user in pending_users:
                    isPending = "true"

                # check if is in rejected list of event
                rejected = Event.query.filter_by(id=event.id).first().rejected
                if user in rejected:
                    isRejected = "true"

                # check if is invited list of event
                invited = Event.query.filter_by(id=event.id).first().invited
                if user in invited:
                    isInvited = "true"

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
                    "isHosting": isHosting,
                    "isPending": isPending,
                    "isInvited": isInvited,
                    "isRejected": isRejected,
                    "isAccepted": isAccepted,
                    "slotsLeft": event.maxGuests - len(accepted_users),
                    "URL": event.URL
                })
            self.result = event_list
            return True
        except Exception as exception:
            self.result = "Event doesn't exist."
            return False

    def get_pending_event_list(self, user):  #
        try:
            from models import Event, User
            event_set = User.query.filter_by(id=user.id).first().pending
            event_list = []
            for event in event_set:
                isHosting = "false"
                isAccepted = "false"
                isPending = "false"
                isRejected = "false"
                isInvited = "false"

                # check if is hosting the event
                host_user = User.query.filter_by(id=event.host).first()
                if host_user.accessToken == user.accessToken:
                    isHosting = "true"

                # check if is in accepted list of event
                accepted_users = Event.query.filter_by(id=event.id).first().accepted
                if user in accepted_users:
                    isAccepted = "true"

                # check if is pending list of event
                pending_users = Event.query.filter_by(id=event.id).first().pending
                if user in pending_users:
                    isPending = "true"

                # check if is in rejected list of event
                rejected = Event.query.filter_by(id=event.id).first().rejected
                if user in rejected:
                    isRejected = "true"

                # check if is invited list of event
                invited = Event.query.filter_by(id=event.id).first().invited
                if user in invited:
                    isInvited = "true"

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
                    "isHosting": isHosting,
                    "isPending": isPending,
                    "isInvited": isInvited,
                    "isRejected": isRejected,
                    "isAccepted": isAccepted,
                    "slotsLeft": event.maxGuests - len(accepted_users),
                    "URL": event.URL
                })
            self.result = event_list
            return True
        except Exception as exception:
            self.result = "Event doesn't exist."
            return False

    def get_invited_event_list(self, user):  #
        try:
            from models import Event, User
            event_set = User.query.filter_by(id=user.id).first().invited
            event_list = []
            for event in event_set:
                isHosting = "false"
                isAccepted = "false"
                isPending = "false"
                isRejected = "false"
                isInvited = "false"

                # check if is hosting the event
                host_user = User.query.filter_by(id=event.host).first()
                if host_user.accessToken == user.accessToken:
                    isHosting = "true"

                # check if is in accepted list of event
                accepted_users = Event.query.filter_by(id=event.id).first().accepted
                if user in accepted_users:
                    isAccepted = "true"

                # check if is pending list of event
                pending_users = Event.query.filter_by(id=event.id).first().pending
                if user in pending_users:
                    isPending = "true"

                # check if is in rejected list of event
                rejected = Event.query.filter_by(id=event.id).first().rejected
                if user in rejected:
                    isRejected = "true"

                # check if is invited list of event
                invited = Event.query.filter_by(id=event.id).first().invited
                if user in invited:
                    isInvited = "true"

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
                    "isHosting": isHosting,
                    "isPending": isPending,
                    "isInvited": isInvited,
                    "isRejected": isRejected,
                    "isAccepted": isAccepted,
                    "slotsLeft": event.maxGuests - len(accepted_users),
                    "URL": event.URL
                })
            self.result = event_list
            return True
        except Exception as exception:
            self.result = "Event doesn't exist."
            return False

    def get_upcoming_events(self, user):  #
        try:
            from models import Event, User
            from datetime import datetime

            event_set = Event.query.filter(Event.startDate > datetime.now())

            event_list = []
            for event in event_set:

                isHosting = "false"
                isAccepted = "false"
                isPending = "false"
                isRejected = "false"
                isInvited = "false"

                # check if is hosting the event
                host_user = User.query.filter_by(id=event.host).first()
                if host_user.accessToken == user.accessToken:
                    isHosting = "true"

                # check if is in accepted list of event
                accepted_users = Event.query.filter_by(id=event.id).first().accepted
                if user in accepted_users:
                    isAccepted = "true"

                # check if is pending list of event
                pending_users = Event.query.filter_by(id=event.id).first().pending
                if user in pending_users:
                    isPending = "true"

                # check if is in rejected list of event
                rejected = Event.query.filter_by(id=event.id).first().rejected
                if user in rejected:
                    isRejected = "true"

                # check if is invited list of event
                invited = Event.query.filter_by(id=event.id).first().invited
                if user in invited:
                    isInvited = "true"

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
                    "isHosting": isHosting,
                    "isPending": isPending,
                    "isInvited": isInvited,
                    "isRejected": isRejected,
                    "isAccepted": isAccepted,
                    "slotsLeft": event.maxGuests - len(accepted_users),
                    "URL": event.URL
                })
            self.result = event_list
            return True

        except Exception as exception:
            self.result = "Event doesn't exist."
            return False

    def get_user_lists(self, event_id):  #
        try:
            from models import Event, User

            acceptedUsers = Event.query.filter_by(id=event_id).first().accepted
            rejectedUsers = Event.query.filter_by(id=event_id).first().rejected
            invitedUsers = Event.query.filter_by(id=event_id).first().invited
            pendingUsers = Event.query.filter_by(id=event_id).first().pending

            acceptedList = []
            rejectedList = []
            invitedList = []
            pendingList = []

            for user in acceptedUsers:
                new_user = {
                    "name": user.name,
                    "email": user.email,
                    "pic": user.photoLink
                }
                acceptedList.append(new_user)

            for user in rejectedUsers:
                new_user = {
                    "name": user.name,
                    "email": user.email,
                    "pic": user.photoLink
                }
                rejectedList.append(new_user)

            for user in invitedUsers:
                new_user = {
                    "name": user.name,
                    "email": user.email,
                    "pic": user.photoLink
                }
                invitedList.append(new_user)

            for user in pendingUsers:
                new_user = {
                    "name": user.name,
                    "email": user.email,
                    "pic": user.photoLink
                }
                pendingList.append(new_user)

            complete_list = {
                "usersAccepted": acceptedList,
                "usersInvited": invitedList,
                "usersPending": pendingList,
                "usersRejected": rejectedList
            }

            self.result = complete_list
            return True

        except Exception as exception:
            self.result = "ERROR getting lists"
            return False

    def get_available_users(self, event_id):  #
        try:
            from models import Event, User

            acceptedUsers = Event.query.filter_by(id=event_id).first().accepted
            rejectedUsers = Event.query.filter_by(id=event_id).first().rejected
            invitedUsers = Event.query.filter_by(id=event_id).first().invited
            pendingUsers = Event.query.filter_by(id=event_id).first().pending
            host_id = Event.query.filter_by(id=event_id).first().host
            host = User.query.filter_by(id=host_id).first()

            allUsers = User.query.all()

            toDelete = []

            for i in range(len(acceptedUsers)):
                for j in range(len(allUsers)):
                    if acceptedUsers[i].id == allUsers[j].id:
                        toDelete.append(j)

            for i in range(len(rejectedUsers)):
                for j in range(len(allUsers)):
                    if rejectedUsers[i].id == allUsers[j].id:
                        toDelete.append(j)

            for i in range(len(invitedUsers)):
                for j in range(len(allUsers)):
                    if invitedUsers[i].id == allUsers[j].id:
                        toDelete.append(j)

            for i in range(len(pendingUsers)):
                for j in range(len(allUsers)):
                    if pendingUsers[i].id == allUsers[j].id:
                        toDelete.append(j)

            for i in range(len(allUsers)):
                if allUsers[i].id == host.id:
                    toDelete.append(i)

            for i in list(set(toDelete)):
                allUsers.pop(i)

            availableUsers = []
            for user in allUsers:
                new_user = {
                    "name": user.name,
                    "email": user.email,
                    "pic": user.photoLink
                }
                availableUsers.append(new_user)

            self.result = availableUsers
            return True
        except Exception as e:
            self.result = "ERROR getting available users"
            return False
