from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SubmitField
from wtforms.validators import Required, Email

class SignupForm(Form):
    email = TextField(u'email', validators = [Required(),Email()])


