from ast import Store
from cgi import print_exception
from ctypes import addressof
from dataclasses import dataclass
from unicodedata import category
from venv import create
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime

from boardgame_app.models import Publisher, Boardgame, User, Post, UserMixin, user_boardgame
from boardgame_app.forms import PublisherForm, BoardgameForm, SignUpForm, LoginForm, PostForm
# Import app and db from events_app package so that we can run app
from boardgame_app.extensions import app, db
from flask_login import login_user, logout_user, current_user, login_required
from boardgame_app import bcrypt

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)

# source venv/bin/activate
# which python
# python3 app.py
# export FLASK_ENV=development
# export FLASK_DEBUG=1
# flask run

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    publishers = Publisher.query.all()
    boardgames = Boardgame.query.all()
    return render_template('home.html', publishers=publishers, boardgames=boardgames)

@main.route('/new_publisher', methods=['GET', 'POST'])
@login_required
def new_publisher():

    form = PublisherForm()
    if form.validate_on_submit():
        create_new_publisher = Publisher(
            company = form.company.data,
            description = form.description.data,
            created_by = current_user
        )
        db.session.add(create_new_publisher)
        db.session.commit()
        flash("You have created a new Publisher")
        return redirect(url_for("main.publisher_detail", publisher_id=create_new_publisher.id))

    return render_template('new_publisher.html', form=form)

@main.route('/new_boardgame', methods=['GET', 'POST'])
@login_required
def new_boardgame():

    form = BoardgameForm()
    if form.validate_on_submit():
        create_new_boardgame = Boardgame(
            name = form.name.data,
            category = form.category.data,
            photo_url = form.photo_url.data,
            publisher = form.publisher.data,
            created_by = current_user
            )
        db.session.add(create_new_boardgame)
        db.session.commit()
        flash("You have added a new Boardgame")
        return redirect(url_for("main.publisher_detail", publisher_id=create_new_boardgame.publisher_id))

    return render_template('new_boardgame.html', form=form)

@main.route('/publisher/<publisher_id>', methods=['GET', 'POST'])
def publisher_detail(publisher_id):
    publisher = Publisher.query.get(publisher_id)

    form = PublisherForm(obj=publisher)
    
    if form.validate_on_submit():
        publisher.company = form.company.data
        publisher.description = form.description.data
        db.session.add(publisher)
        db.session.commit()
        flash("Publisher Updated.")
        return redirect(url_for('main.publisher_detail', publisher_id=publisher.id))

    return render_template('publisher_detail.html', publisher=publisher, form=form)

@main.route('/boardgame/<boardgame_id>', methods=['GET', 'POST'])
def boardgame_detail(boardgame_id):
    boardgame = Boardgame.query.get(boardgame_id)
    form = BoardgameForm(obj=boardgame)
    post_form = PostForm()

    if post_form.validate_on_submit():
      post = Post(
        poster = current_user,
        posts = post_form.post.data,
        boardgame = boardgame
      )
      db.session.add(post)
      db.session.commit()

      return redirect(url_for('main.boardgame_detail', boardgame_id=boardgame_id))

    if form.validate_on_submit():
        boardgame.name = form.name.data
        boardgame.category = form.category.data
        boardgame.photo_url = form.photo_url.data
        boardgame.publisher = form.publisher.data

        db.session.add(boardgame)
        db.session.commit()
        flash("You have added this boardgame to the publisher list.")
        return redirect(url_for('main.boardgame_detail', boardgame_id=boardgame.id))        

    # return render_template('boardgame_detail.html', boardgame=boardgame, form=form)
    return render_template('boardgame_detail.html', boardgame=boardgame, form=form, post_form=post_form)

@main.route('/add_to_user_boardgame/<boardgame_id>', methods=['POST'])
@login_required
def add_to_user_boardgame(boardgame_id):
    boardgame = Boardgame.query.get(boardgame_id)
    current_user.user_boardgame_users.append(boardgame)
    db.session.add(current_user)
    db.session.commit()
    flash("Boardgame added to user list")
    return redirect(url_for('main.user_boardgame', boardgame_id=boardgame.id)) 


@main.route('/user_boardgame')
@login_required
def user_boardgame():
    user_boardgame = current_user.user_boardgame_users
    return render_template("user_boardgame.html", user_boardgame=user_boardgame)

# AUTH
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))

