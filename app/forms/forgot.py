from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ForgotPassword(FlaskForm):    
    email_address = StringField('Email Address', validators=[DataRequired()])
    submit = SubmitField('Submit')