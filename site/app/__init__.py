from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.pagedown import PageDown

app = Flask(__name__)
app.config.from_object('config')

lm = LoginManager(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
pagedown = PageDown(app)

from app import views, models
