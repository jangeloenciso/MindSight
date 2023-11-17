from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, DateField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class EditStudentForm(FlaskForm):
    # Fields from StudentInformation model
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    course = StringField('Course', validators=[DataRequired(), Length(max=100)])
    year_level = SelectField('Year Level', choices=[('1st Year', '1st Year'), ('2nd Year', '2nd Year'), ('3rd Year', '3rd Year'), ('4th Year', '4th Year'), ('5th Year', '5th Year')])
    gpa = FloatField('GPA')
    campus = SelectField('Campus', choices=[('Boni', 'Boni'), ('Pasig', 'Pasig')])

    # Fields from PersonalInformation model
    age = IntegerField('Age')
    sex = SelectField('Sex', choices=[('Male', 'Male'), ('Female', 'Female')])
    gender = StringField('Gender', validators=[Length(max=20)])
    contact_number = StringField('Contact Number', validators=[Length(max=20)])
    religion = StringField('Religion', validators=[Length(max=50)])
    date_of_birth = DateField('Date of Birth')
    place_of_birth = StringField('Place of Birth', validators=[Length(max=100)])
    nationality = StringField('Nationality', validators=[Length(max=50)])
    counseling_history = StringField('Counseling History', validators=[Length(max=100)])
    residence = StringField('Residence', validators=[Length(max=100)])

    # Fields from FamilyBackground model
    father_age = IntegerField('Father Age')
    mother_age = IntegerField('Mother Age')
    father_last_name = StringField('Father Last Name', validators=[Length(max=50)])
    mother_last_name = StringField('Mother Last Name', validators=[Length(max=50)])
    father_first_name = StringField('Father First Name', validators=[Length(max=50)])
    mother_first_name = StringField('Mother First Name', validators=[Length(max=50)])

    # Fields from HealthInformation model
    height = FloatField('Height')
    weight = FloatField('Weight')
    sight = StringField('Sight', validators=[Length(max=20)])
    hearing = StringField('Hearing', validators=[Length(max=20)])
    speech = StringField('Speech', validators=[Length(max=20)])
    general_health = StringField('General Health', validators=[Length(max=100)])
    experienced_sickness = StringField('Experienced Sickness', validators=[Length(max=3)])

    # Fields from EducationalBackground model
    senior_high_school = StringField('Senior High School', validators=[Length(max=100)])
    shs_strand = StringField('SHS Strand', validators=[Length(max=100)])
    shs_graduation_year = IntegerField('SHS Graduation Year')
    junior_high_school = StringField('Junior High School', validators=[Length(max=100)])
    jhs_graduation_year = IntegerField('JHS Graduation Year')
    elementary_school = StringField('Elementary School', validators=[Length(max=100)])
    elementary_graduation_year = IntegerField('Elementary Graduation Year')

    # Fields from PsychologicalAssessments model
    learning_styles = StringField('Learning Styles', validators=[Length(max=100)])
    personality_test = StringField('Personality Test', validators=[Length(max=100)])
    iq_test = StringField('IQ Test', validators=[Length(max=100)])


    submit = SubmitField('Update')
