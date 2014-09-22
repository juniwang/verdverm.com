from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.bcrypt import generate_password_hash

from flask.ext.assets import Environment, Bundle, ManageAssets

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

assets = Environment(app)
manager.add_command("assets", ManageAssets(assets))

js = Bundle('js/verdverm/posts.js',
            filters='jsmin', output='js/verdverm.js')
assets.register('js_all', js)

from app import views, models
from app.user.models import UserBasic
from app.auth.models import UserAuth
from app.auth import constants as USER
from app.posts.models import Post, Comment


@manager.command
def runapp():
    app.run(host='0.0.0.0', port=5000, debug=True)



@manager.command
def dbfill():
    # if the admin user is not created, create one
    user = UserBasic.query.filter_by(email="tony@verdverm.com").first()
    if user is None:
        au = UserBasic(email="tony@verdverm.com", nickname = "verdverm")
        bu = UserBasic(email="tony@iassic.com", nickname = "tony")
        db.session.add(au)
        db.session.add(bu)
        
        aa = UserAuth(user_id=1,
            hpass=generate_password_hash("verdverm"),
            role=USER.ADMIN,
            status=USER.ACTIVE )
        db.session.add(aa)

        ba = UserAuth(user_id=2,
            hpass=generate_password_hash("iassic"),
            role=USER.USER,
            status=USER.ACTIVE )
        db.session.add(ba)

        db.session.commit()

