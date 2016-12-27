
class AccountBean(object):

    def new_account(self, name, accessToken):
        try:
            from models import User
            from application import db
            c = User(name=name, accessToken=accessToken)
            db.session.add(c)
            db.session.commit()
            self.result = "Account created."
            return True
        except Exception as e:
            self.result = "Account already exists."
            return False

    def update_account(self, name, accessToken):
        try:
            from models import User
            from application import db
            Token.query.filter_by(token=self.token).first()