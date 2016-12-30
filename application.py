# coding=utf-8
from flask import Flask
from flask import request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/thirdparty'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app, session_options={'autocommit': False})

db.engine.dialect.supports_sane_rowcount = db.engine.dialect.supports_sane_multi_rowcount = False

from routes import *
from models import *

try:
    db.create_all()
    db.session.commit()
    print "Models created."
except Exception as e:
    print "Models already created."

if __name__ == '__main__':
    app.run()
