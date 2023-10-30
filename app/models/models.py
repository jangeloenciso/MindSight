from flask_login import UserMixin
from app import db
import re
from sqlalchemy import event
from sqlalchemy.orm import validates
from . import courses

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, first_name, last_name, username, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password 

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False 

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f'<User {self.username}>'
    


class College(db.Model):
    __tablename__ = 'colleges'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    courses = db.relationship('Course', backref='college', lazy=True)

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'))


class StudentInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    year_level = db.Column(db.String(20))
    gpa = db.Column(db.Float)
    campus = db.Column(db.String(20), nullable=False)

    @validates('student_id')
    def validate_student_id(self, key, value):
        if not re.match(r'^20\d{2}-\d{6}$', value):
            raise ValueError("Student ID must be in the format 20xx-xxxxxx")
        return value


    personal_information = db.relationship('PersonalInformation', backref='student', uselist=False)

    family_background = db.relationship('FamilyBackground', backref='student', uselist=False)

    health_information = db.relationship('HealthInformation', backref='student', uselist=False)

    educational_background = db.relationship('EducationalBackground', backref='student', uselist=False)

    psychological_assessments = db.relationship('PsychologicalAssessments', backref='student', uselist=False)


class PersonalInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    sex = db.Column(db.String(10))
    gender = db.Column(db.String(20))
    contact_number = db.Column(db.String(20))
    religion = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)
    place_of_birth = db.Column(db.String(100))
    nationality = db.Column(db.String(50))
    counseling_history = db.Column(db.String(100))
    residence = db.Column(db.String(100))
    student_id = db.Column(db.String(20), db.ForeignKey('student_information.student_id'))

class FamilyBackground(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    father_age = db.Column(db.Integer)
    mother_age = db.Column(db.Integer)
    father_last_name = db.Column(db.String(50))
    mother_last_name = db.Column(db.String(50))
    father_first_name = db.Column(db.String(50))
    mother_first_name = db.Column(db.String(50))
    student_id = db.Column(db.String(20), db.ForeignKey('student_information.student_id'))

class HealthInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    sight = db.Column(db.String(20))
    hearing = db.Column(db.String(20))
    speech = db.Column(db.String(20))
    general_health = db.Column(db.String(100))
    experienced_sickness = db.Column(db.String(3))
    student_id = db.Column(db.String(20), db.ForeignKey('student_information.student_id'))

class EducationalBackground(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    senior_high_school = db.Column(db.String(100))
    shs_strand = db.Column(db.String(100))
    shs_graduation_year = db.Column(db.Integer)
    junior_high_school = db.Column(db.String(100))
    jhs_graduation_year = db.Column(db.Integer)
    elementary_school = db.Column(db.String(100))
    elementary_graduation_year = db.Column(db.Integer)
    student_id = db.Column(db.String(20), db.ForeignKey('student_information.student_id'))

class PsychologicalAssessments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    learning_styles = db.Column(db.String(100))
    personality_test = db.Column(db.String(100))
    iq_test = db.Column(db.String(100))
    student_id = db.Column(db.String(20), db.ForeignKey('student_information.student_id'))
