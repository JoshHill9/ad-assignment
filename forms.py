import sys
sys.path.append('lib')
sys.path.append('models')
sys.path.append('controllers')

from flask_wtf import FlaskForm, csrf
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError

import UserController

def validate_password(form, password):
    validators = {"upper": False, "lower": False, "digit": False}
    for letter in password.data:
        if letter.isupper():
            validators["upper"] = True
        if letter.islower():
            validators["lower"] = True
        if letter.isdigit():
            validators["digit"] = True
    if not(validators["upper"] and validators["lower"] and validators["digit"]):
        raise ValidationError("Password must contain atleast: one uppercase, one lowercase character and one digit.")

class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=20, message="Username should be between 4 and 20 characters long.")])
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=30, message="Password should be between 8 and 30 characters long."), validate_password])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo("password")])

    submit = SubmitField("Register")

    def validate_username(self, username):
        if UserController.get_user(username=username.data):
            raise ValidationError("This username is already in use. Please select a new one.")

    def validate_email(self, email):
        if UserController.get_user(email=email.data):
            raise ValidationError("This email address is already in use. Please login instead.")


class LoginForm(FlaskForm):

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

    login = SubmitField("Login")

    def validate_username(self, username):
        if not UserController.get_user(username=username.data):
            raise ValidationError("This account does not exists. Please re-enter an existing account username.")

class PasswordResetForm(FlaskForm):

    old_password = PasswordField("Old Password", validators=[InputRequired(), Length(min=8, max=30, message="Password length is incorrect")])

    new_password = PasswordField("New Password", validators=[InputRequired(), Length(min=8, max=30, message="Password should be between 8 and 30 characters long."), validate_password])
    confirm_new_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo("new_password")])

    reset = SubmitField("Change Password")


class SearchForm(FlaskForm):

    search_term = StringField("Search Term", validators=[InputRequired()])
    search_location = SelectField("Available In", choices=[("uk", "UK"), ("us", "US")], validators=[InputRequired()])

    search = SubmitField("Perform Search")
