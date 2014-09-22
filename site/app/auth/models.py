# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from app.models import Base
from app.auth import constants as USER

class UserAuth(Base):

    __tablename__ = 'user_auth'

    hpass = db.Column(db.LargeBinary)
    role = db.Column(db.SmallInteger, default=USER.USER)
    status = db.Column(db.SmallInteger, default=USER.NEW)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user_basic.id'))


    def is_authenticated(self):
        return True

    def is_active(self):
        return self.status != USER.INACTIVE

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def get_role(self):
        return self.role

    def __repr__(self):
        return '<User %r>' % (self.nickname)
