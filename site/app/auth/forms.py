from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required, Email


class RegisterForm(Form):
    email = TextField(u'email', validators = [Required(),Email()])
    password = PasswordField(u'password', validators = [Required()])
    password_confirm = PasswordField(u'password', validators = [Required()])

class LoginForm(Form):
    email = TextField(u'email', validators = [Required(),Email()])
    password = PasswordField(u'password', validators = [Required()])
    remember_me = BooleanField(u'remember_me', default = False)
