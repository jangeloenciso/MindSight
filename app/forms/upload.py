from app import app
import os
from flask import request, Blueprint
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, Form

class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")

# def upload_file(form):
