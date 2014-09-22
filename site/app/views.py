from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import current_user, login_required

from app import app, db, lm, bcrypt
from forms import SignupForm

from app.auth import constants as USER
from app.auth.controllers import *
from app.posts.controllers import *

@lm.user_loader
def load_user(id):
    return UserAuth.query.filter_by(user_id = int(id)).first()

@app.before_request
def before_request():
    g.auth = current_user
    if g.auth is not None and not g.auth.is_anonymous():
        g.user = UserBasic.query.get(g.auth.user_id)
        if g.auth.role is USER.ADMIN:
            g.admin = g.auth


@app.errorhandler(404)
def not_found(error):
    return render_template("errors/404.html")

@app.errorhandler(400)
def not_found(error):
    print error
    return render_template("errors/400.html")


@app.route('/')
@app.route('/index')
def index():
    auth = g.auth
    user = None
    admin = None
    if hasattr(g, 'user'):
        user = g.user
    if hasattr(g, 'admin'):
        admin = g.admin
    return render_template("index.html", user=user, admin=admin)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if g.auth is not None and g.auth.is_authenticated():
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


