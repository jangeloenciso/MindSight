from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import bcrypt
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object('config.Config')  # Load your app configuration

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

from app.models import User  # Import the User model after initializing db
