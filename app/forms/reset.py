from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class ResetPassword(FlaskForm):    
    security_answer = StringField('Security Answer', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=7)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')