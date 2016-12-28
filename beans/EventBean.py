class EventBean(object):
    # TODO: Just an example
    def create_event(self):
        try:
            from models import User
            from application import db
            u = User(name=name, accessToken=accessToken, email=email)
            db.session.add(u)
            db.session.commit()
            self.result = "Account created."
            return True
        except Exception as e:
            self.update_account(name, accessToken, email)
            return False
