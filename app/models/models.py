from flask_login import UserMixin
from app import db
import re
from sqlalchemy import event
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash
from datetime import datetime
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
    security_question = db.Column(db.String(255), nullable=False)
    security_answer = db.Column(db.String(255), nullable=False)

    def __init__(self, first_name, last_name, username, email, password, role, security_question, security_answer):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.security_question = security_question
        self.security_answer = security_answer

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
    


class BasicInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    college = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=True)
    year_level = db.Column(db.Integer)
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

    student_signature = db.Column(db.LargeBinary)

    submitted_on = db.Column(db.DateTime, default=datetime.now)


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

    referral_information = db.relationship('ReferralInformation', backref='student', uselist=False)

    case_note = db.relationship('CaseNote', backref='student')

    sessions = db.relationship('Sessions', backref='student')

    documents = db.relationship('Document', backref='basic_information', lazy=True)


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
    previous_treatments = db.Column(db.String(10))
    previous_treatments_likes_dislikes = db.Column(db.String(400))
    previous_treatments_learned = db.Column(db.String(400))
    previous_treatments_like_to_continue = db.Column(db.String(400))

    previous_hospital_stays_psych = db.Column(db.String(10))
    current_thoughts_to_harm = db.Column(db.String(10))
    past_thoughts_to_harm = db.Column(db.String(10))
    
    student_id = db.Column(db.String(20), db.ForeignKey('basic_information.student_id'))

    
class HealthInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    medication_and_dose = db.Column(db.String(100))

    # ch = childhood
    serious_ch_illnesses_history = db.Column(db.String(100))

    head_injuries = db.Column(db.String(10))
    lose_consciousness = db.Column(db.String(10))
    convulsions_or_seizures = db.Column(db.String(10))
    fever = db.Column(db.String(10))
    allergies = db.Column(db.String(10))
    
    current_physical_health = db.Column(db.String(20)) 
    last_check_up = db.Column(db.Date) # idk date ba dapat???
    has_physician = db.Column(db.String(10))
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
    rel_qual_other = db.Column(db.String(50), nullable=True)

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
    satisfaction = db.Column(db.String(500), nullable=True)
    satisfaction_reason = db.Column(db.String(500), nullable=True)

    student_id = db.Column(db.String(20), db.ForeignKey('basic_information.student_id'))

class SubstanceAbuseHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # TODO:

    struggled_with_substance_abuse = db.Column(db.String(10))

    # alcohol
    alcohol = db.Column(db.String(50), nullable=True)
    alcohol_age_first_use = db.Column(db.String(50), nullable=True)
    alcohol_frequency_of_use = db.Column(db.String(50), nullable=True)
    alcohol_amount_used = db.Column(db.String(50), nullable=True)
    alcohol_way_of_intake = db.Column(db.String(50), nullable=True)

    # cigarette
    cigarette = db.Column(db.String(50), nullable=True)
    cigarette_age_first_use = db.Column(db.String(50), nullable=True)
    cigarette_frequency_of_use = db.Column(db.String(50), nullable=True)
    cigarette_amount_used = db.Column(db.String(50), nullable=True)
    cigarette_way_of_intake = db.Column(db.String(50), nullable=True)

    # marijuana
    marijuana = db.Column(db.String(50), nullable=True)
    marijuana_age_first_use = db.Column(db.String(50), nullable=True)
    marijuana_frequency_of_use = db.Column(db.String(50), nullable=True)
    marijuana_amount_used = db.Column(db.String(50), nullable=True)
    marijuana_way_of_intake = db.Column(db.String(50), nullable=True)


    # cocaine
    cocaine = db.Column(db.String(50), nullable=True)
    cocaine_age_first_use = db.Column(db.String(50), nullable=True)
    cocaine_frequency_of_use = db.Column(db.String(50), nullable=True)
    cocaine_amount_used = db.Column(db.String(50), nullable=True)
    cocaine_way_of_intake = db.Column(db.String(50), nullable=True)


    # heroin
    heroin = db.Column(db.String(50), nullable=True)
    heroin_age_first_use = db.Column(db.String(50), nullable=True)
    heroin_frequency_of_use = db.Column(db.String(50), nullable=True)
    heroin_amount_used = db.Column(db.String(50), nullable=True)
    heroin_way_of_intake = db.Column(db.String(50), nullable=True)


    # amphetamines
    amphetamines = db.Column(db.String(50), nullable=True)
    amphetamines_age_first_use = db.Column(db.String(50), nullable=True)
    amphetamines_frequency_of_use = db.Column(db.String(50), nullable=True)
    amphetamines_amount_used = db.Column(db.String(50), nullable=True)
    amphetamines_way_of_intake = db.Column(db.String(50), nullable=True)


    # club_drugs
    club_drugs = db.Column(db.String(50), nullable=True)
    club_drugs_age_first_use = db.Column(db.String(50), nullable=True)
    club_drugs_frequency_of_use = db.Column(db.String(50), nullable=True)
    club_drugs_amount_used = db.Column(db.String(50), nullable=True)
    club_drugs_way_of_intake = db.Column(db.String(50), nullable=True)


    # pain_meds
    pain_meds = db.Column(db.String(50), nullable=True)
    pain_meds_age_first_use = db.Column(db.String(50), nullable=True)
    pain_meds_frequency_of_use = db.Column(db.String(50), nullable=True)
    pain_meds_amount_used = db.Column(db.String(50), nullable=True)
    pain_meds_way_of_intake = db.Column(db.String(50), nullable=True)


    # benzodiazepines
    benzo = db.Column(db.String(50), nullable=True)
    benzo_age_first_use = db.Column(db.String(50), nullable=True)
    benzo_frequency_of_use = db.Column(db.String(50), nullable=True)
    benzo_amount_used = db.Column(db.String(50), nullable=True)
    benzo_way_of_intake = db.Column(db.String(50), nullable=True)

    # hallucinogens
    hallucinogens = db.Column(db.String(50), nullable=True)
    hallucinogens_age_first_use = db.Column(db.String(50), nullable=True)
    hallucinogens_frequency_of_use = db.Column(db.String(50), nullable=True)
    hallucinogens_amount_used = db.Column(db.String(50), nullable=True)
    hallucinogens_way_of_intake = db.Column(db.String(50), nullable=True)

    # others
    other_meds = db.Column(db.String(50), nullable=True)
    other_meds_age_first_use = db.Column(db.String(50), nullable=True)
    other_meds_frequency_of_use = db.Column(db.String(50), nullable=True)
    other_meds_amount_used = db.Column(db.String(50), nullable=True)
    other_meds_way_of_intake = db.Column(db.String(50), nullable=True)

    treatment_program_name = db.Column(db.String(50), nullable=True)
    treatment_type = db.Column(db.String(50), nullable=True)
    treatment_date = db.Column(db.String(50), nullable=True)
    treatment_outcome = db.Column(db.String(100), nullable=True)

    student_id = db.Column(db.String(20), db.ForeignKey('basic_information.student_id'))

class LegalHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # TODO:

    pending_criminal_charges = db.Column(db.String(10))
    on_probation = db.Column(db.String(10))
    has_been_arrested = db.Column(db.String(10))

    convictions = db.relationship('Conviction', backref='legal_history', lazy=True)

    student_id = db.Column(db.String(20), db.ForeignKey('basic_information.student_id'))

class Conviction(db.Model):
    __tablename__ = 'convictions'

    id = db.Column(db.Integer, primary_key=True)

    # TODO: THIS WAS LAZY. FOR TESTING PURPOSES ONLY. CREATE SEPARATE MODEL/TABLE LATER
    conviction = db.Column(db.String(50), nullable=True)
    conviction_date = db.Column(db.Date(), nullable=True)
    conviction_outcome = db.Column(db.String(50), nullable=True)

    legal_history_id = db.Column(db.Integer, db.ForeignKey('legal_history.id'), nullable=False)


class AdditionalInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # add to form and route
    nature_of_concern = db.Column(db.String(50), nullable=True)
    counselor = db.Column(db.String(50), nullable=True)
    personal_agreement = db.Column(db.Boolean, default=False)
    personal_agreement_date = db.Column(db.DateTime)

    referral_source = db.Column(db.String(50))

    emergency_name = db.Column(db.String(50))
    emergency_relationship = db.Column(db.String(50))
    emergency_address = db.Column(db.String(50))
    emergency_contact = db.Column(db.String(50))

    to_work_on = db.Column(db.String(500))
    expectations = db.Column(db.String(500))
    things_to_change = db.Column(db.String(500))
    other_information = db.Column(db.String(500))

    status = db.Column(db.String(20))
    remarks = db.Column(db.String(30))

    student_id = db.Column(db.String(20), db.ForeignKey('basic_information.student_id'))

# TODO: Add this, also figure out if you're going to separate it or not
class ReferralInformation(db.Model):
    __tablename__ = 'referral_information'

    id = db.Column(db.Integer, primary_key=True)

    reason_for_referral = db.Column(db.String(500), nullable=True)
    receiving_agency = db.Column(db.String(100), nullable=True)
    receiving_contact_number = db.Column(db.String(20), nullable=True)
    receiving_name = db.Column(db.String(40), nullable=True)
    receiving_email = db.Column(db.String(40), nullable=True)
    office_address = db.Column(db.String(50), nullable=True)
    appointment_schedule = db.Column(db.DateTime, nullable=True)
    
    client_signature = db.Column(db.LargeBinary)
    client_signature_date = db.Column(db.Date)
    counselor_signature = db.Column(db.LargeBinary)
    counselor_signature_date = db.Column(db.Date)

    student_id = db.Column(db.String(20), db.ForeignKey('basic_information.student_id'))

class CaseNote(db.Model):
    __tablename__ = 'case_note'

    id = db.Column(db.Integer, primary_key=True)

    counselor_name = db.Column(db.String(100), nullable=True)
    interview_date = db.Column(db.Date)
    number_of_session = db.Column(db.String(100))

    subject_complaint = db.Column(db.String(500))
    objective_assessment = db.Column(db.String(500))
    plan_of_action = db.Column(db.String(500))
    progress_made = db.Column(db.String(500))

    student_id = db.Column(db.String(20), db.ForeignKey('basic_information.student_id'))


class Sessions(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    
    session_date = db.Column(db.Date())
    session_time_start = db.Column(db.Time())
    session_time_end = db.Column(db.Time())
    session_follow_up = db.Column(db.String(500))
    session_attended_by = db.Column(db.String(500))

    student_id = db.Column(db.String(20), db.ForeignKey('basic_information.student_id'))

    # Plan of action, recommendation, if for follow up or not,


    # Please ignore
class Document(db.Model):
    __tablename__ = 'documents'

    file_id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=True)
    path = db.Column(db.String(255), nullable=True)

    student_id = db.Column(db.String(20), db.ForeignKey('basic_information.student_id'))

    def __init__(self, filename, path, student_id):
        self.filename = filename
        self.path = path
        self.student_id = student_id