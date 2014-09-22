from app import db
from app.models import Base

class Post(Base):

    __tablename__ = 'post'

    title = db.Column(db.String(256), unique = True)
    textbody = db.Column(db.LargeBinary)
    htmlbody = db.Column(db.LargeBinary)
    draft = db.Column(db.Boolean, default = True)

    user_id = db.Column(db.Integer, db.ForeignKey('user_basic.id'))
    comments = db.relationship('Comment', backref = 'post', lazy = 'dynamic')

    def __repr__(self):
        return '<Post %r>' % (self.body)

class Comment(Base):

    __tablename__ = 'comment'

    textbody = db.Column(db.LargeBinary)
    htmlbody = db.Column(db.LargeBinary)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user_basic.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return '<Comment %r>' % (self.body)
