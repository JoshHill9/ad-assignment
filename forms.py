import sys
sys.path.append('lib')
from flask_wtf import FlaskForm, csrf
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
