from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional

class EditCredentials(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(message="Please enter your first name"), Length(min=2, max=80, message="First name must be between 2 and 80 characters")])
    last_name = StringField('Last Name', validators=[DataRequired(message="Please enter your last name"), Length(min=2, max=80, message="Last name must be between 2 and 80 characters")])
    username = StringField('Username', validators=[DataRequired(message="Please enter your username"), Length(min=2, max=80, message="Username must be between 2 and 80 characters")])
    email = StringField('Email', validators=[DataRequired(message="Please enter your email"), Email(message="Please enter a valid email address")])
    password = PasswordField('New password', validators=[Optional(), Length(min=7, message="Password must be at least 7 characters long")])
    confirm = PasswordField('Confirm new password', validators=[Optional(), EqualTo('password', message="Passwords must match")])
    current_password = PasswordField('Old password', validators=[Optional()])
    security_question = SelectField('Security Question', choices=[
        ('question1', 'In what city did your parents meet?'),
        ('question2', 'Where did you go on your first solo trip?'),
        ('question3', 'What was the first dish you learned to cook?'),
        ('question4', 'What was the name of your first stuffed toy?'),
        ('question5', 'What was the title of the first book you read?')
    ], validators=[DataRequired()])
    security_answer = StringField('Security Answer', validators=[Optional()])
    submit = SubmitField('Update')
    