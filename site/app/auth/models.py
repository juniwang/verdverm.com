# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from app.models import Base

ROLE_NULL = 0
ROLE_USER = 1
ROLE_ADMIN = 2

class UserAuth(Base):
    id = db.Column(db.Integer, primary_key = True)
    hpass = db.Column(db.LargeBinary)
    role = db.Column(db.SmallInteger, default = ROLE_NULL)
    active = db.Column(db.Boolean, default = False)
    activated = db.Column(db.Boolean, default = False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def get_role(self):
        return self.role

    def __repr__(self):
        return '<User %r>' % (self.nickname)
