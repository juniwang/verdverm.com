from flask import render_template, flash, redirect, session, url_for, request, g, make_response

from app.auth import constants as USER

from app.posts.models import Post, Comment
from app.posts.forms import PostForm

from app import app, db

import sys


@app.route('/posts')
def posts():
    auth = g.auth
    user = None
    admin = None
    if hasattr(g, 'user'):
        user = g.user
    if g.auth is not None and auth.is_anonymous():
        user = None
    if hasattr(g, 'admin'):
        admin = g.admin

    posts = [ {'title':p.title,'body':str(p.htmlbody)} for p in Post.query.order_by(Post.title).all()]


    # posts = [ # fake array of posts
    #     {
    #         'author': { 'nickname': 'John' },
    #         'body': 'Beautiful day in Portland!'
    #     },
    #     {
    #         'author': { 'nickname': 'Susan' },
    #         'body': 'The Avengers movie was so cool!'
    #     }
    # ]
    return render_template("posts/posts.html",
        user = user,
        admin = admin,
        posts = posts)

@app.route('/posts/edit', methods = ['GET', 'POST'])
def editpost():
    if g.auth is not None and g.auth.role is not USER.ADMIN:
        return redirect(url_for('not_found'))

    user = g.user
    admin = g.admin

    if request.method == 'POST':
        try: 
            form = request.args

            print >> sys.stderr, form

            post = Post()
            post.user_id = user.id

            post.title = form.get('title')
            post.textbody = form.get('textbody').encode('u8')
            post.htmlbody = form.get('htmlbody').encode('u8')

            db.session.add(post)
            db.session.commit()

            return make_response("Post Saved")
        except:
            print >> sys.stderr, sys.exc_info()
            return make_response("Exceptional Error") 

    form = PostForm()
    form.drafts.choices = [(p.id,p.title) for p in Post.query.filter_by(draft=True).order_by(Post.title).all()]

    return render_template("posts/editpost.html",
        form = form, 
        user = user,
        admin = admin)



