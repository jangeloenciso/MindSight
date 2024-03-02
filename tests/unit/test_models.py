from app.models.models import *
from werkzeug.security import check_password_hash

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    user = User('John', 'Doe', 'johndoe', 'johndoe@example.com', 'password123', 'admin')
    assert user.first_name == 'John'
    assert user.last_name == 'Doe'
    assert user.username == 'johndoe'
    assert user.email == 'johndoe@example.com'
    assert user.password != 'password123'
    assert user.role == 'admin'