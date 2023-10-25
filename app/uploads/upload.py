from app import app
from flask import request, Blueprint
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(filename):
    if 'file' in request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(app.config['UPLOAD_FOLDER'])
        return 'FILE UPLOADED SUCCESSFULLY!'
    return 'No file uploaded'