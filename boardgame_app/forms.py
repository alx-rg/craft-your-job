from tokenize import String
from unicodedata import name
from flask_wtf import FlaskForm
from sqlalchemy import Float
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField, PasswordField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from boardgame_app.models import Publisher, Boardgame, ItemCategory, User, PublisherCategory
from wtforms.validators import DataRequired, Length, URL, ValidationError
from boardgame_app import bcrypt

class PublisherForm(FlaskForm):
    """Form for adding/updating a Publisher."""
    company = StringField('Publisher Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = StringField("Who and What is this BoardGame Published")
    publisher_category = SelectField("Category", choices=PublisherCategory.choices())
    submit = SubmitField("Create New Publisher")

class BoardgameForm(FlaskForm):
    """Form for adding/updating a Boardgame."""
    name = StringField('Boardgame Name', validators=[DataRequired(), Length(min=2, max=100)])
    category = SelectField("Category", choices=ItemCategory.choices())
    photo_url = StringField("Photo of Product URL")
    submit = SubmitField("Create New Boardgame")
    publisher = QuerySelectField("Publisher", query_factory=lambda: Publisher.query, allow_blank=False)
    submit = SubmitField("Create New Boardgame")


# SIGN UP BELOW ++++++++++++++++++++++++++++++++++++++++

class SignUpForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user with that username. Please try again.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')