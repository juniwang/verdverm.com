from app import db
# from sqlalchemy.dialects.postgresql import JSON

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())



ROLE_NULL = 0
ROLE_USER = 1
ROLE_ADMIN = 2

class UserBasic(Base):
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    maillist = db.Column(db.Boolean, default = False)
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
