from ast import Store
from cgi import print_exception
from ctypes import addressof
from dataclasses import dataclass
from unicodedata import category
from venv import create
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime

from boardgame_app.models import Publisher, Boardgame, User, UserMixin, user_boardgame
from boardgame_app.forms import PublisherForm, BoardgameForm, SignUpForm, LoginForm
# Import app and db from events_app package so that we can run app
from boardgame_app.extensions import app, db
from flask_login import login_user, logout_user, current_user, login_required
from boardgame_app import bcrypt

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_boardgames = Boardgame.query.all()
    return render_template('home.html', all_boardgames=all_boardgames)

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
        flash("You have created a new Boardgame")
        return redirect(url_for("main.publisher_detail", publisher_id=create_new_boardgame.publisher_id))

    return render_template('new_boardgame.html', form=form)