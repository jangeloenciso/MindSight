from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class EditCredentials(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(message="Please enter your first name"), Length(min=2, max=80, message="First name must be between 2 and 80 characters")])
    last_name = StringField('Last Name', validators=[DataRequired(message="Please enter your last name"), Length(min=2, max=80, message="Last name must be between 2 and 80 characters")])
    username = StringField('Username', validators=[DataRequired(message="Please enter your username"), Length(min=2, max=80, message="Username must be between 2 and 80 characters")])
    email = StringField('Email', validators=[DataRequired(message="Please enter your email"), Email(message="Please enter a valid email address")])
    password = PasswordField('New password', validators=[DataRequired(message="Please enter your new password"), Length(min=7, message="Password must be at least 7 characters long")])
    confirm = PasswordField('Confirm new password', validators=[DataRequired(message="Please confirm your new password"), EqualTo('password', message="Passwords must match")])
    current_password = PasswordField('Old password', validators=[DataRequired(message="Please enter your old password")])
    submit = SubmitField('Update')
    