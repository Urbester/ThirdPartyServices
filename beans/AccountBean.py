class AccountBean(object):
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
            self.update_account(name, accessToken, email, photoLink)
            return False

    def update_account(self, name, accessToken, email, photoLink):
        try:
            from models import User
            from application import db
            u = User.query.filter_by(email=self.email).first()
            u.accessToken = accessToken
            db.session.commit()
            self.result = "Account updated."
        except Exception as e:
            self.result = "Account error."
            return False

    def delete_account(self, accessToken):
        try:
            from models import User
            from application import db
            u = User.query.filter_by(accessToken=self.accessToken).first()
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
            u = User.query.filter_by(accessToken=self.accessToken).first()
            self.result = {"email": u.email, "accessToken": u.accessToken, "name": u.name, "photoLink": u.photoLink}
            return True
        except Exception as e:
            self.result = "Account doesn't exist."
            return False
