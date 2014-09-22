from app import db
from app.models import Base

class UserBasic(Base):

    __tablename__ = 'user_basic'

    nickname = db.Column(db.String(64))
    email = db.Column(db.String(120), unique = True)
    maillist = db.Column(db.Boolean, default = False)

    auth = db.relationship('UserAuth', backref = 'user_basic', lazy = 'joined')
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    comments = db.relationship('Comment', backref = 'author', lazy = 'dynamic')

    def get_id(self):
        return unicode(self.id)
