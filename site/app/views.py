from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import current_user, login_required

from app import app, db, lm, bcrypt
from forms import PageDownFormExample, SignupForm
from app.auth.models import ROLE_ADMIN

from app.auth.controllers import *

@lm.user_loader
def load_user(id):
    return UserBasic.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    if not g.user.is_anonymous() and g.user.role is ROLE_ADMIN:
        g.admin = g.user


@app.route('/')
@app.route('/index')
def index():
    user = g.user
    admin = None
    if user.is_anonymous():
        user = None
    if hasattr(g, 'admin'):
        admin = g.admin
    return render_template("index.html", user=user, admin=admin)

@app.route('/posts')
def posts():

    user = g.user
    if user.is_anonymous():
        user = None

    form = PageDownFormExample()

    posts = [ # fake array of posts
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("posts.html",
        user = user,
        posts = posts,
        form = form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))

    form = SignupForm()

    if form.validate_on_submit():

        user = None
        user = UserBasic.query.filter_by(email = form.email.data).first()

        if user:
            flash('That email address is already in use.')
            return redirect(url_for('signup'))

        user = UserBasic(email=form.email.data,
                    nickname = form.email.data.split('@')[0],
                    maillist=True )
        db.session.add(user)
        db.session.commit()

        if user:
            flash('Signup successful.')
            return redirect(url_for('index'))
        else:
            flash('Failed to signup user...')
            return redirect(url_for('signup'))

    return render_template('maillist/signup.html', form=form)


