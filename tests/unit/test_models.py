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
    assert user.password == 'password123'
    assert user.role == 'admin'

def test_sibling_association_with_family_background():
    """
    GIVEN a FamilyBackground Model
    WHEN a new Sibling is created
    THEN check the relationships between Siblings, FamilyBackground, and BasicInformation
    """

    family_background = FamilyBackground(
        birth_location='Sample Location', 
        raised_by='Sample Parent'
        )

    basic_information = BasicInformation(
        student_id='2012-123456',
        last_name='Doe',
        first_name='John',
        course='Computer Science',
        year_level='Senior',
        campus='Main',
        date_of_birth='2000-01-01',
        age=24,
        gender='Male',
        civil_status='Single',
        nationality='American',
        religion='Christian',
        residence='123 Street Name, City',
        contact_number='1234567890',
        phone_number='0987654321',
        email_address='johndoe@example.com',
        guardian_name='Jane Doe',
        guardian_address='456 Street Name, City',
        guardian_contact='9876543210',
        family_background = family_background
    )

    sibling1 = Sibling(name='Sibling 1', age=20, gender='Male', rel_qual='Brother', family_background=family_background)
    sibling2 = Sibling(name='Sibling 2', age=18, gender='Female', rel_qual='Sister', family_background=family_background)

    assert sibling1.family_background == family_background
    assert sibling2.family_background == family_background

    assert sibling1.family_background == basic_information.family_background

    assert basic_information.family_background.siblings == [sibling1, sibling2]

    assert family_background.siblings == [sibling1, sibling2]