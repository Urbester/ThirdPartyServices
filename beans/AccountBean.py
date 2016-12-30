class AccountBean(object):

    def __init__(self):
        pass

    def new_account(self, name, accessToken, email, photoLink):
        try:
            from models import User
            from application import db
            u = User(name=name, accessToken=accessToken, email=email, photoLink=photoLink)
            db.session.add(u)
            db.session.commit()
            self.result = "Account created."
            return True
        except Exception as e:
            db.session.rollback()
            db.session.remove()
            if self.update_account(name, accessToken, email, photoLink):
                return True
            return False

    def update_account(self, name, accessToken, email, photoLink):
        try:
            from models import User
            from application import db
            u = User.query.filter_by(email=email).first()
            u.accessToken = accessToken
            db.session.commit()
            self.result = "Account updated."
            return True
        except Exception as e:
            self.result = "Account error."
            return False

    def delete_account(self, accessToken):
        try:
            from models import User
            from application import db
            u = User.query.filter_by(accessToken=accessToken).first()
            db.session.delete(u)
            db.session.commit()
            self.result = "Account removed."
            return True
        except Exception as e:
            self.result = "Account doesn't exist."
            return False

    def get_account(self, accessToken):
        try:
            from models import User
            u = User.query.filter_by(accessToken=accessToken).first()
            self.result = {"email": u.email, "accessToken": u.accessToken, "name": u.name, "photoLink": u.photoLink}
            return True
        except Exception as e:
            self.result = "Account doesn't exist."
            return False
