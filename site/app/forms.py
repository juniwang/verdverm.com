from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SubmitField
from wtforms.validators import Required, Email
from flask.ext.pagedown.fields import PageDownField

class PageDownFormExample(Form):
    pagedown = PageDownField('Enter your markdown')
    submit = SubmitField('Submit')

class SignupForm(Form):
    email = TextField(u'email', validators = [Required(),Email()])


