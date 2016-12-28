from flask import Flask
from flask.ext.cors import CORS
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

application = Flask(__name__)
CORS(application)

application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1:3306/thirdparty'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application, session_options={'autocommit': False})

db.engine.dialect.supports_sane_rowcount = db.engine.dialect.supports_sane_multi_rowcount = False

@app.route('/v1/')
def status():
    return 'Status: Online'

from routes.accounts import *

if __name__ == '__main__':
    try:
        from models import *
        db.create_all()
        db.session.commit()
        print "Models created."
    except Exception as e:
        print "Models already created."
    app.run()
