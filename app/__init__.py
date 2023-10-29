from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object("config.Config")

from app import routes

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)