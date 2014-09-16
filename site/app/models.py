from app import db
# from sqlalchemy.dialects.postgresql import JSON 

ROLE_NULL = 0
ROLE_USER = 1
ROLE_ADMIN = 2

class UserBasic(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    hpass = db.Column(db.LargeBinary)
    role = db.Column(db.SmallInteger, default = ROLE_NULL)
    maillist = db.Column(db.Boolean, default = False)
    active = db.Column(db.Boolean, default = False)
    activated = db.Column(db.Boolean, default = False)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

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


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    textbody = db.Column(db.LargeBinary)
    htmlbody = db.Column(db.LargeBinary)
    timestamp = db.Column(db.DateTime)
    posted = db.Column(db.Boolean, default = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_basic.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)