from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.pagedown import PageDown
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.bcrypt import generate_password_hash
import os

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

lm = LoginManager(app)
bcrypt = Bcrypt(app)
pagedown = PageDown(app)

from app import views, models

@manager.command
def dbfill():
    # if the admin user is not created, create one
    user = UserBasic.query.filter_by(email="tony@verdverm.com").first()
    if user is None:
        a = UserBasic(email="tony@verdverm.com", nickname = "verdverm",
                                        hpass=generate_password_hash("verdverm"),
                                        role=ROLE_ADMIN )
        b = UserBasic(email="tony@iassic.com", nickname = "tony",
                                        hpass=generate_password_hash("iassic"),
                                        role=ROLE_USER )
        db.session.add(a)
        db.session.add(b)
        db.session.commit()

