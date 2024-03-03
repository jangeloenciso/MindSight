from flask_login import UserMixin
from app import db
import re
from sqlalchemy import event
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash
from . import courses

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(45), nullable=False)

    def __init__(self, first_name, last_name, username, email, password, role):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password
        self.role = role

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
    name = db.Column(db.String(100), nullable=True)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'))


class BasicInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    year_level = db.Column(db.String(20))
    campus = db.Column(db.String(20), nullable=False)

    date_of_birth = db.Column(db.Date)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    civil_status = db.Column(db.String(20))
    nationality = db.Column(db.String(50))
    religion = db.Column(db.String(50))
    residence = db.Column(db.String(100))
    contact_number = db.Column(db.String(20))
    phone_number = db.Column(db.String(20))
    email_address = db.Column(db.String(120), nullable=False)

    guardian_name = db.Column(db.String(50), nullable=True)
    guardian_address = db.Column(db.String(50), nullable=True)
    guardian_contact = db.Column(db.String(20), nullable=True)


    @validates('student_id')
    def validate_student_id(self, key, value):
        if not re.match(r'^20\d{2}-\d{6}$', value):
            raise ValueError("Student ID must be in the format 20xx-xxxxxx")
        return value
    

    history_information = db.relationship('HistoryInformation', backref='student', uselist=False)

    health_information = db.relationship('HealthInformation', backref='student', uselist=False)

    family_background = db.relationship('FamilyBackground', backref='student', uselist=False)

    social_history = db.relationship('SocialHistory', backref='student', uselist=False)

    educational_background = db.relationship('EducationalBackground', backref='student', uselist=False)

    occupational_history = db.relationship('OccupationalHistory', backref='student', uselist=False)

    substance_abuse_history = db.relationship('SubstanceAbuseHistory', backref='student', uselist=False)

    legal_history = db.relationship('LegalHistory', backref='student', uselist=False)

    additional_information = db.relationship('AdditionalInformation', backref='student', uselist=False)

    visits = db.relationship('StudentVisits', backref='student')


class HistoryInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    information_provider = db.Column(db.String(50))

    current_problem = db.Column(db.String(200))
    problem_length = db.Column(db.String(200))
    
    stressors = db.Column(db.String(200))
    
    # Checkbox fields
    substance_abuse = db.Column(db.Boolean, default=False)
    addiction = db.Column(db.Boolean, default=False)
    depression_sad_down_feelings = db.Column(db.Boolean, default=False)
    high_low_energy_level = db.Column(db.Boolean, default=False)
    angry_irritable = db.Column(db.Boolean, default=False)
    loss_of_interest = db.Column(db.Boolean, default=False)
    difficulty_enjoying_things = db.Column(db.Boolean, default=False)
    crying_spells = db.Column(db.Boolean, default=False)
    decreased_motivation = db.Column(db.Boolean, default=False)
    withdrawing_from_people = db.Column(db.Boolean, default=False)
    mood_swings = db.Column(db.Boolean, default=False)
    black_and_white_thinking = db.Column(db.Boolean, default=False)
    negative_thinking = db.Column(db.Boolean, default=False)
    change_in_weight_or_appetite = db.Column(db.Boolean, default=False)
    change_in_sleeping_pattern = db.Column(db.Boolean, default=False)
    suicidal_thoughts_or_plans = db.Column(db.Boolean, default=False)
    self_harm = db.Column(db.Boolean, default=False)
    homicidal_thoughts_or_plans = db.Column(db.Boolean, default=False)
    difficulty_focusing = db.Column(db.Boolean, default=False)
    feelings_of_hopelessness = db.Column(db.Boolean, default=False)
    feelings_of_shame_or_guilt = db.Column(db.Boolean, default=False)
    feelings_of_inadequacy = db.Column(db.Boolean, default=False)
    anxious_nervous_tense_feelings = db.Column(db.Boolean, default=False)
    panic_attacks = db.Column(db.Boolean, default=False)
    racing_or_scrambled_thoughts = db.Column(db.Boolean, default=False)
    bad_or_unwanted_thoughts = db.Column(db.Boolean, default=False)
    flashbacks_or_nightmares = db.Column(db.Boolean, default=False)
    muscle_tensions_aches = db.Column(db.Boolean, default=False)
    hearing_voices_or_seeing_things = db.Column(db.Boolean, default=False)
    thoughts_of_running_away = db.Column(db.Boolean, default=False)
    paranoid_thoughts = db.Column(db.Boolean, default=False)
    feelings_of_frustration = db.Column(db.Boolean, default=False)
    feelings_of_being_cheated = db.Column(db.Boolean, default=False)
    perfectionism = db.Column(db.Boolean, default=False)
    counting_washing_checking = db.Column(db.Boolean, default=False)
    distorted_body_image = db.Column(db.Boolean, default=False)
    concerns_about_dieting = db.Column(db.Boolean, default=False)
    loss_of_control_over_eating = db.Column(db.Boolean, default=False)
    binge_eating_or_purging = db.Column(db.Boolean, default=False)
    rules_about_eating = db.Column(db.Boolean, default=False)
    compensating_for_eating = db.Column(db.Boolean, default=False)
    excessive_exercise = db.Column(db.Boolean, default=False)
    indecisiveness_about_career = db.Column(db.Boolean, default=False)
    job_problems = db.Column(db.Boolean, default=False)
    other = db.Column(db.String(100))
    
    # TODO: Add other fields for the rest of the history information
    previous_treatments = db.Column(db.Boolean, default=False)
    previous_treatments_likes_dislikes = db.Column(db.String(400))
    previous_treatments_learned = db.Column(db.String(400))
    previous_treatments_like_to_continue = db.Column(db.String(400))

    previous_hospital_stays_psych = db.Column(db.Boolean, default=False)
    current_thoughts_to_harm = db.Column(db.Boolean, default=False)
    past_thoughts_to_harm = db.Column(db.Boolean, default=False)
    
    student_id = db.Column(db.String(20), db.ForeignKey('basic_information.student_id'))

    
class HealthInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    medication_and_dose = db.Column(db.String(100))

    # ch = childhood
    serious_ch_illnesses_history = db.Column(db.String(100))

    head_injuries = db.Column(db.Boolean, default=False)
    lose_consciousness = db.Column(db.Boolean, default=False)
    convulsions_or_seizures = db.Column(db.Boolean, default=False)
    fever = db.Column(db.Boolean, default=False)
    allergies = db.Column(db.String(100))
    
    current_physical_health = db.Column(db.String(20)) 
    last_check_up = db.Column(db.Date) # idk date ba dapat???
    has_physician = db.Column(db.Boolean, default=False)
    physician_name = db.Column(db.String(50))
    physician_email = db.Column(db.String(50))
    physician_number = db.Column(db.String(20))

    student_id = db.Column(db.String(20), db.ForeignKey('basic_information.student_id'))

# idk how to add siblings and shit 
class FamilyBackground(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # TODO: ADD TO FLASK FORMS
    birth_location = db.Column(db.String(50))
    raised_by = db.Column(db.String(50))

    rel_qual_mother = db.Column(db.String(50), nullable=True)
    rel_qual_father = db.Column(db.String(50), nullable=True)
    rel_qual_step_parent = db.Column(db.String(50), nullable=True)

    family_abuse_history = db.Column(db.String(300), nullable=True)
    family_mental_history = db.Column(db.String(300), nullable=True)
    additional_information = db.Column(db.String(300), nullable=True)

    siblings = db.relationship('Sibling', backref='family_background', lazy=True)

    student_id = db.Column(db.String(20), db.ForeignKey('basic_information.student_id'))

class Sibling(db.Model):
    __tablename__ = 'siblings'
    
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    rel_qual = db.Column(db.String(50), nullable=True)

    # TODO: FIX THIS ??? NOT SURE LMAO
    family_background_id = db.Column(db.Integer, db.ForeignKey('family_background.id'), nullable=False)


class SocialHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    relationship_with_peers = db.Column(db.String(300))
    social_support_network = db.Column(db.String(300))
    hobbies_or_interests = db.Column(db.String(300))
    cultural_concerns = db.Column(db.String(300))

    student_id = db.Column(db.String(20), db.ForeignKey('basic_information.student_id'))

class EducationalBackground(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    educational_history = db.Column(db.String(40))
    highest_level_achieved = db.Column(db.String(40))
    additional_information = db.Column(db.String(200))

    student_id = db.Column(db.String(20), db.ForeignKey('basic_information.student_id'))

class OccupationalHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # TODO:
    employment_status = db.Column(db.String(20))
    satisfaction = db.Column(db.String(20), nullable=True)
    satisfaction_reason = db.Column(db.String(200), nullable=True)

    student_id = db.Column(db.String(20), db.ForeignKey('basic_information.student_id'))

class SubstanceAbuseHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # TODO:

    struggled_with_substance_abuse = db.Column(db.Boolean, default=False)

    # alcohol
    alcohol = db.Column(db.Boolean, default=False)
    alcohol_age_first_use = db.Column(db.String(50))
    alcohol_frequency_of_use = db.Column(db.String(50))
    alcohol_amount_used = db.Column(db.String(50))
    alcohol_way_of_intake = db.Column(db.String(50))

    # cigarette
    cigarette = db.Column(db.Boolean, default=False)
    cigarette_age_first_use = db.Column(db.String(50))
    cigarette_frequency_of_use = db.Column(db.String(50))
    cigarette_amount_used = db.Column(db.String(50))
    cigarette_way_of_intake = db.Column(db.String(50))

    # marijuana
    marijuana = db.Column(db.Boolean, default=False)
    marijuana_age_first_use = db.Column(db.String(50))
    marijuana_frequency_of_use = db.Column(db.String(50))
    marijuana_amount_used = db.Column(db.String(50))
    marijuana_way_of_intake = db.Column(db.String(50))


    # cocaine
    cocaine = db.Column(db.Boolean, default=False)
    cocaine_age_first_use = db.Column(db.String(50))
    cocaine_frequency_of_use = db.Column(db.String(50))
    cocaine_amount_used = db.Column(db.String(50))
    cocaine_way_of_intake = db.Column(db.String(50))


    # heroin
    heroin = db.Column(db.Boolean, default=False)
    heroin_age_first_use = db.Column(db.String(50))
    heroin_frequency_of_use = db.Column(db.String(50))
    heroin_amount_used = db.Column(db.String(50))
    heroin_way_of_intake = db.Column(db.String(50))


    # amphetamines
    amphetamines = db.Column(db.Boolean, default=False)
    amphetamines_age_first_use = db.Column(db.String(50))
    amphetamines_frequency_of_use = db.Column(db.String(50))
    amphetamines_amount_used = db.Column(db.String(50))
    amphetamines_way_of_intake = db.Column(db.String(50))


    # club_drugs
    club_drugs = db.Column(db.Boolean, default=False)
    club_drugs_age_first_use = db.Column(db.String(50))
    club_drugs_frequency_of_use = db.Column(db.String(50))
    club_drugs_amount_used = db.Column(db.String(50))
    club_drugs_way_of_intake = db.Column(db.String(50))


    # pain_meds
    pain_meds = db.Column(db.Boolean, default=False)
    pain_meds_age_first_use = db.Column(db.String(50))
    pain_meds_frequency_of_use = db.Column(db.String(50))
    pain_meds_amount_used = db.Column(db.String(50))
    pain_meds_way_of_intake = db.Column(db.String(50))


    # benzodiazepines
    benzo = db.Column(db.Boolean, default=False)
    benzo_age_first_use = db.Column(db.String(50))
    benzo_frequency_of_use = db.Column(db.String(50))
    benzo_amount_used = db.Column(db.String(50))
    benzo_way_of_intake = db.Column(db.String(50))

    # hallucinogens
    hallucinogens = db.Column(db.Boolean, default=False)
    hallucinogens_age_first_use = db.Column(db.String(50))
    hallucinogens_frequency_of_use = db.Column(db.String(50))
    hallucinogens_amount_used = db.Column(db.String(50))
    hallucinogens_way_of_intake = db.Column(db.String(50))

    # others
    other_meds = db.Column(db.Boolean, default=False)
    other_meds_age_first_use = db.Column(db.String(50))
    other_meds_frequency_of_use = db.Column(db.String(50))
    other_meds_amount_used = db.Column(db.String(50))
    other_meds_way_of_intake = db.Column(db.String(50))

    treatment_program_name = db.Column(db.String(50), nullable=True)
    treatment_type = db.Column(db.String(50), nullable=True)
    treatment_date = db.Column(db.Date)
    treatment_outcome = db.Column(db.String(100))

    student_id = db.Column(db.String(20), db.ForeignKey('basic_information.student_id'))

class LegalHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # TODO:

    pending_criminal_charges = db.Column(db.Boolean, default=False)
    on_probation = db.Column(db.Boolean, default=False)
    has_been_arrested = db.Column(db.Boolean, default=False)

    # TODO: THIS WAS LAZY. FOR TESTING PURPOSES ONLY. CREATE SEPARATE MODEL/TABLE LATER
    conviction = db.Column(db.String(50))
    conviction_date = db.Date
    conviction_outcome = db.Column(db.String(50))

    student_id = db.Column(db.String(20), db.ForeignKey('basic_information.student_id'))

class AdditionalInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # add to form and route
    nature_of_concern = db.Column(db.String(50), nullable=True)
    counselor = db.Column(db.String(50), nullable=True)
    personal_agreement = db.Column(db.Boolean, default=False)

    referral_source = db.Column(db.String(50))

    emergency_name = db.Column(db.String(50))
    emergency_relationship = db.Column(db.String(50))
    emergency_address = db.Column(db.String(50))
    emergency_contact = db.Column(db.String(50))

    to_work_on = db.Column(db.String(500))
    expectations = db.Column(db.String(500))
    things_to_change = db.Column(db.String(500))
    other_information = db.Column(db.String(500))

    student_id = db.Column(db.String(20), db.ForeignKey('basic_information.student_id'))

# TODO: Add this, also figure out if you're going to separate it or not
# class ReferralInformation(db.Model):
    

class StudentVisits(db.Model):
    __tablename__ = 'student_visits'

    visit_id = db.Column(db.Integer, primary_key=True)
    date_of_visit = db.Column(db.Date, nullable=False)
    nature_of_concern = db.Column(db.String(100))

    student_id = db.Column(db.String(20), db.ForeignKey('basic_information.student_id'))

    # Plan of action, recommendation, if for follow up or not,