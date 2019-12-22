import sys
sys.path.append('lib')
sys.path.append('models')
sys.path.append('controllers')

from flask_wtf import FlaskForm, csrf
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

import UserController

class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirmPassword = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])

    submit = SubmitField("Register")

    def validate_username(self, username):
        if UserController.getUser(username=username.data):
            raise ValidationError("This username is already in use. Please select a new one.")

    def validate_email(self, email):
        if UserController.getUser(email=email.data):
            raise ValidationError("This email address is already in use. Please login instead.")



class LoginForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    login = SubmitField("Login")

    def validate_username(self, username):
        if not UserController.getUser(username=username.data):
            raise ValidationError("This account does not exists. Please re-enter an existing account username.")

class ShowSearchForm(FlaskForm):
    search_term = StringField("Seach Term", validators=[DataRequired()])
    search_location = SelectField("Available In", choices=[("uk", "UK"), ("us", "US")], validators=[DataRequired()])

    search = SubmitField("Perform Search")
