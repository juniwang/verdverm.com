from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required, Email


class PostForm(Form):
    drafts = SelectField(u'draft', coerce=int)
    title = TextField(u'title')
    textbody = TextAreaField(u'textbody')
    htmlbody = TextAreaField(u'htmlbody')
    dopost = BooleanField(u'dopost')

class CommentForm(Form):
    textbody = TextAreaField(u'textbody')
    htmlbody = TextAreaField(u'htmlbody')
