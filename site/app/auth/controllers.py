from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.bcrypt import check_password_hash, generate_password_hash


from app.user.models import UserBasic

from app.auth.models import UserAuth
from app.auth.forms import LoginForm, RegisterForm
from app.auth import constants as USER

from app import app, db, bcrypt


@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.auth is not None and g.auth.is_authenticated():
        return redirect(url_for('index'))

    form = RegisterForm()

    if form.validate_on_submit():

        if form.password.data != form.password_confirm.data:
            flash('Your passwords were not the same.')
            return redirect(url_for('register'))


        user = None
        auth = None
        user = UserBasic.query.filter_by(email = form.email.data).first()

        if user and user.role == USER.MAILLIST:
            user.nickname = form.email.data.split('@')[0]
            user.maillist=True
            
            auth = UserAuth()
            auth.hpass  = bcrypt.generate_password_hash(form.password.data)
            auth.role   = USER.USER
            auth.status = USER.NEW

            db.session.commit()
            return redirect(url_for('index'))
        else:
            flash('That email address is already in use.')
            return redirect(url_for('register'))

        user = UserBasic(email=form.email.data,
                    nickname = form.email.data.split('@')[0],
                    maillist=True)
        
        auth = UserAuth()
        auth.hpass  = bcrypt.generate_password_hash(form.password.data)
        auth.role   = USER.USER
        auth.status = USER.NEW

        db.session.add(user)
        db.session.add(auth)
        db.session.commit()

        if auth:
            flash('Registration successful.')
            return redirect(url_for('index'))

        else:
            flash('Failed to register user...')
    return render_template('auth/register.html', form=form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.auth is not None and g.auth.is_authenticated():
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = UserBasic.query.filter_by( email=form.email.data ).first()
        if user:
            auth = UserAuth.query.filter_by( user_id = user.id ).first()
            if auth and bcrypt.check_password_hash(auth.hpass, form.password.data):
                g.auth = auth
                session[user.id] = user.id
                login_user(auth)
                session['remember_me'] = form.remember_me.data
                flash("Logged in successfully.")
                return redirect(request.args.get("next") or url_for("index"))
        else:
            flash("Invalid Login")

    return render_template('auth/login.html', form = form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.")
    return redirect(url_for('index'))
