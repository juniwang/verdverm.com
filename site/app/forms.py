from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email
from flask.ext.pagedown.fields import PageDownField

class PageDownFormExample(Form):
    pagedown = PageDownField('Enter your markdown')
    submit = SubmitField('Submit')

class LoginForm(Form):
    email = TextField(u'email', validators = [Required(),Email()])
    password = PasswordField(u'password', validators = [Required()])
    remember_me = BooleanField(u'remember_me', default = False)

class SignupForm(Form):
    email = TextField(u'email', validators = [Required(),Email()])

class RegisterForm(Form):
    email = TextField(u'email', validators = [Required(),Email()])
    password = PasswordField(u'password', validators = [Required()])
    password_confirm = PasswordField(u'password', validators = [Required()])

