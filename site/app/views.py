from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.bcrypt import check_password_hash, generate_password_hash

from app import app, db, lm, bcrypt
from forms import PageDownFormExample, LoginForm, SignupForm, RegisterForm
from models import UserBasic, ROLE_NULL, ROLE_USER, ROLE_ADMIN
import sys


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

    return render_template('signup.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))

    form = RegisterForm()

    if form.validate_on_submit():

        if form.password.data != form.password_confirm.data:
            flash('Your passwords were not the same.')
            return redirect(url_for('register'))


        user = None
        user = UserBasic.query.filter_by(email = form.email.data).first()

        if user and user.role == ROLE_NULL:
            user.nickname = form.email.data.split('@')[0]
            user.hpass=bcrypt.generate_password_hash(form.password.data)
            user.maillist=True
            user.active=True
            user.role=ROLE_USER
            db.session.commit()
            return redirect(url_for('index'))
        else:
            flash('That email address is already in use.')
            return redirect(url_for('register'))

        user = UserBasic(email=form.email.data,
                    nickname = form.email.data.split('@')[0],
                    hpass=bcrypt.generate_password_hash(form.password.data),
                    maillist=True,
                    active=True,
                    role=ROLE_USER )
        db.session.add(user)
        db.session.commit()
    
        if user:
            flash('Registration successful.')
            return redirect(url_for('index'))
        
        else:
            flash('Failed to register user...')
    return render_template('register.html', form=form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))

    form = LoginForm()
    
    if form.validate_on_submit():
        user = UserBasic.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.hpass, form.password.data):
            session[user.id] = user.id
            login_user(user)
            session['remember_me'] = form.remember_me.data
            flash("Logged in successfully.")
            return redirect(request.args.get("next") or url_for("index"))
        else:
            flash("Invalid Login")
    return render_template('login.html', form = form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
