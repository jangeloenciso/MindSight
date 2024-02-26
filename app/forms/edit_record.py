from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, DateField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class EditStudentForm(FlaskForm):
    # Fields from StudentInformation model
    student_id = StringField('Student ID', validators=[DataRequired(), Length(min=11, max=11)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    course = StringField('Course', validators=[DataRequired(), Length(max=100)])
    year_level = StringField('Year Level', validators=[Length(max=20)])
    gpa = FloatField('GPA')
    campus = StringField('Campus', validators=[DataRequired(), Length(max=20)])

    # Fields from PersonalInformation model
    age = IntegerField('Age')
    sex = StringField('Sex', validators=[Length(max=10)])
    gender = StringField('Gender', validators=[Length(max=20)])
    contact_number = StringField('Contact Number', validators=[Length(max=20)])
    religion = StringField('Religion', validators=[Length(max=50)])
    date_of_birth = DateField('Date of Birth')
    place_of_birth = StringField('Place of Birth', validators=[Length(max=100)])
    nationality = StringField('Nationality', validators=[Length(max=50)])
    counseling_history = StringField('Counseling History', validators=[Length(max=100)])
    residence = StringField('Residence', validators=[Length(max=100)])
    civil_status = StringField('Civil Status', validators=[Length(max=20)])  # New field

    # Fields from HistoryInformation model
    information_provider = StringField('Information Provider', validators=[Length(max=50)])
    current_problem = StringField('Current Problem', validators=[Length(max=200)])
    problem_length = StringField('Problem Length', validators=[Length(max=200)])
    stressors = StringField('Stressors', validators=[Length(max=200)])
    # Add checkboxes for all boolean fields

    # Fields from HealthInformation model
    medication_and_dose = StringField('Medication and Dose', validators=[Length(max=100)])
    serious_ch_illnesses_history = StringField('Serious CH Illnesses History', validators=[Length(max=100)])
    head_injuries = StringField('Head Injuries', validators=[Length(max=100)])
    lose_consciousness = StringField('Loss of Consciousness', validators=[Length(max=100)])
    convulsions_or_seizures = StringField('Convulsions or Seizures', validators=[Length(max=100)])
    fever = StringField('Fever', validators=[Length(max=100)])
    allergies = StringField('Allergies', validators=[Length(max=100)])
    current_physical_health = StringField('Current Physical Health', validators=[Length(max=20)])
    last_check_up = DateField('Last Check-Up')
    has_physician = StringField('Has Physician')
    physician_name = StringField('Physician Name', validators=[Length(max=50)])
    physician_email = StringField('Physician Email', validators=[Length(max=50)])
    physician_number = StringField('Physician Number', validators=[Length(max=20)])

    # Fields from FamilyBackground model
    father_age = IntegerField('Father Age')
    mother_age = IntegerField('Mother Age')
    father_last_name = StringField('Father Last Name', validators=[Length(max=50)])
    mother_last_name = StringField('Mother Last Name', validators=[Length(max=50)])
    father_first_name = StringField('Father First Name', validators=[Length(max=50)])
    mother_first_name = StringField('Mother First Name', validators=[Length(max=50)])
    family_abuse_history = StringField('Family Abuse History', validators=[Length(max=300)])
    family_mental_history = StringField('Family Mental History', validators=[Length(max=300)])
    family_additional_information = StringField('Additional Information', validators=[Length(max=300)])

    # Fields from SocialHistory model
    relationship_with_peers = StringField('Relationship with Peers', validators=[Length(max=300)])
    social_support_network = StringField('Social Support Network', validators=[Length(max=300)])
    hobbies_or_interests = StringField('Hobbies or Interests', validators=[Length(max=300)])
    cultural_concerns = StringField('Cultural Concerns', validators=[Length(max=300)])

    # Fields from EducationalBackground model
    educational_history = StringField('Educational History', validators=[Length(max=40)])
    highest_level_achieved = StringField('Highest Level Achieved', validators=[Length(max=40)])
    educational_additional_information = StringField('Additional Information', validators=[Length(max=200)])

    # Fields from OccupationalHistory model
    employment_status = StringField('Employment Status', validators=[Length(max=20)])
    satisfaction = StringField('Satisfaction', validators=[Length(max=20)])
    satisfaction_reason = StringField('Satisfaction Reason', validators=[Length(max=200)])

    # Fields from SubstanceAbuseHistory model
    struggled_with_substance_abuse = StringField('Struggled with Substance Abuse')
    # Add fields for each substance abuse type

    # Fields from LegalHistory model
    pending_criminal_charges = StringField('Pending Criminal Charges')
    on_probation = StringField('On Probation')
    has_been_arrested = StringField('Has Been Arrested')

    # Fields from AdditionalInformation model
    to_work_on = StringField('To Work On', validators=[Length(max=500)])
    expectations = StringField('Expectations', validators=[Length(max=500)])
    things_to_change = StringField('Things to Change', validators=[Length(max=500)])
    other_information = StringField('Other Information', validators=[Length(max=500)])

    submit = SubmitField('Update')
