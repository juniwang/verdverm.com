from app import db
from app.models import Base

class UserBasic(Base):

    __tablename__ = 'user_basic'

    nickname = db.Column(db.String(64))
    email = db.Column(db.String(120), unique = True)
    maillist = db.Column(db.Boolean, default = False)

    auth = db.relationship('UserAuth', backref = 'user_basic', lazy = 'joined')
    posts = db.relationship('Post', backref = 'user_basic', lazy = 'dynamic')
    comments = db.relationship('Comment', backref = 'user_basic', lazy = 'dynamic')

    def is_anonymous(self):
        return True

    def get_id(self):
        return unicode(self.id)
