from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask import g
from flask_login import current_user

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

from .models.models import User

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_user_info():
    user_info = {
        'first_name': current_user.first_name if current_user.is_authenticated else None,
        'last_name': current_user.last_name if current_user.is_authenticated else None,
        'role': current_user.role if current_user.is_authenticated else None
    }
    return user_info

from app import routes

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
