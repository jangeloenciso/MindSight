from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, BooleanField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp

class StudentRecordForm(FlaskForm):
    # # College Information
    # college_name = StringField('College Name', validators=[DataRequired()])
    # Basic Information
    student_id = StringField('Student ID', validators=[DataRequired(), Regexp('^20\d{2}-\d{6}$', message="Student ID must be in the format 20xx-xxxxxx")])
    last_name = StringField('Last Name', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    course = StringField('Course', validators=[DataRequired()])
    year_level = StringField('Year Level', validators=[Optional()])
    campus = StringField('Campus', validators=[DataRequired()])
    
    date_of_birth = DateField('Date of Birth', validators=[Optional()])
    age = IntegerField('Age', validators=[Optional()])
    gender = StringField('Gender', validators=[Optional()])
    civil_status = StringField('Civil Status', validators=[Optional()])
    nationality = StringField('Nationality', validators=[Optional()])
    religion = StringField('Religion', validators=[Optional()])
    residence = StringField('Residence', validators=[Optional()])

    email_address = StringField('Email', validators=[DataRequired(message="Please enter your email"), Email(message="Please enter a valid email address")])
    contact_number = StringField('Contact Number', validators=[Optional()])

    guardian_name = StringField('Guardian Name', validators=[Optional()])
    guardian_address = StringField('Guardian Address', validators=[Optional()])
    guardian_contact = StringField('Guardian Contact', validators=[Optional()])

    # History Information
    information_provider = StringField('Information Provider', validators=[Optional()])

    current_problem = StringField('Current Problem', validators=[Optional()])
    problem_length = StringField('Problem Length', validators=[Optional()])

    stressors = StringField('Stressors', validators=[Optional()])

    substance_abuse = BooleanField('Substance Abuse', validators=[Optional()])
    addiction = BooleanField('Addiction', validators=[Optional()])
    depression_sad_down_feelings = BooleanField('Depression/Sad Down Feelings', validators=[Optional()])
    high_low_energy_level = BooleanField('High/Low Energy Level', validators=[Optional()])
    angry_irritable = BooleanField('Angry/Irritable', validators=[Optional()])
    loss_of_interest = BooleanField('Loss of Interest', validators=[Optional()])
    difficulty_enjoying_things = BooleanField('Difficulty Enjoying Things', validators=[Optional()])
    crying_spells = BooleanField('Crying Spells', validators=[Optional()])
    decreased_motivation = BooleanField('Decreased Motivation', validators=[Optional()])
    withdrawing_from_people = BooleanField('Withdrawing from People', validators=[Optional()])
    mood_swings = BooleanField('Mood Swings', validators=[Optional()])
    black_and_white_thinking = BooleanField('Black and White Thinking', validators=[Optional()])
    negative_thinking = BooleanField('Negative Thinking', validators=[Optional()])
    change_in_weight_or_appetite = BooleanField('Change in Weight or Appetite', validators=[Optional()])
    change_in_sleeping_pattern = BooleanField('Change in Sleeping Pattern', validators=[Optional()])
    suicidal_thoughts_or_plans = BooleanField('Suicidal Thoughts or Plans', validators=[Optional()])
    self_harm = BooleanField('Self-Harm', validators=[Optional()])
    homicidal_thoughts_or_plans = BooleanField('Homicidal Thoughts or Plans', validators=[Optional()])
    difficulty_focusing = BooleanField('Difficulty Focusing', validators=[Optional()])
    feelings_of_hopelessness = BooleanField('Feelings of Hopelessness', validators=[Optional()])
    feelings_of_shame_or_guilt = BooleanField('Feelings of Shame or Guilt', validators=[Optional()])
    feelings_of_inadequacy = BooleanField('Feelings of Inadequacy', validators=[Optional()])
    low_self_esteem = BooleanField('Low Self-Esteem', validators=[Optional()])
    anxious_nervous_tense_feelings = BooleanField('Anxious/Nervous/Tense Feelings', validators=[Optional()])
    panic_attacks = BooleanField('Panic Attacks', validators=[Optional()])
    racing_or_scrambled_thoughts = BooleanField('Racing or Scrambled Thoughts', validators=[Optional()])
    bad_or_unwanted_thoughts = BooleanField('Bad or Unwanted Thoughts', validators=[Optional()])
    flashbacks_or_nightmares = BooleanField('Flashbacks or Nightmares', validators=[Optional()])
    muscle_tensions_aches = BooleanField('Muscle Tensions/Aches', validators=[Optional()])
    hearing_voices_or_seeing_things = BooleanField('Hearing Voices or Seeing Things', validators=[Optional()])
    thoughts_of_running_away = BooleanField('Thoughts of Running Away', validators=[Optional()])
    paranoid_thoughts = BooleanField('Paranoid Thoughts', validators=[Optional()])
    feelings_of_frustration = BooleanField('Feelings of Frustration', validators=[Optional()])
    feelings_of_being_cheated = BooleanField('Feelings of Being Cheated', validators=[Optional()])
    perfectionism = BooleanField('Perfectionism', validators=[Optional()])
    counting_washing_checking = BooleanField('Counting/Washing/Checking', validators=[Optional()])
    distorted_body_image = BooleanField('Distorted Body Image', validators=[Optional()])
    concerns_about_dieting = BooleanField('Concerns About Dieting', validators=[Optional()])
    loss_of_control_over_eating = BooleanField('Loss of Control Over Eating', validators=[Optional()])
    binge_eating_or_purging = BooleanField('Binge Eating or Purging', validators=[Optional()])
    rules_about_eating = BooleanField('Rules About Eating', validators=[Optional()])
    compensating_for_eating = BooleanField('Compensating for Eating', validators=[Optional()])
    excessive_exercise = BooleanField('Excessive Exercise', validators=[Optional()])
    indecisiveness_about_career = BooleanField('Indecisiveness About Career', validators=[Optional()])
    job_problems = BooleanField('Job Problems', validators=[Optional()])
    other_history = StringField('Other', validators=[Optional()])
    previous_treatments = BooleanField('Previous Treatments', validators=[Optional()])
    previous_treatments_likes_dislikes = StringField('Previous Treatments Likes/Dislikes', validators=[Optional()])
    previous_treatments_learned = StringField('Previous Treatments Learned', validators=[Optional()])
    previous_treatments_like_to_continue = StringField('Previous Treatments Like to Continue', validators=[Optional()])
    previous_hospital_stays_psych = BooleanField('Previous Hospital Stays (Psych)', validators=[Optional()])
    current_thoughts_to_harm = BooleanField('Current Thoughts to Harm', validators=[Optional()])
    past_thoughts_to_harm = BooleanField('Past Thoughts to Harm', validators=[Optional()])

    # Health Information
    medication_and_dose = StringField('Medication and Dose', validators=[Optional()])

    serious_ch_illnesses_history = StringField('Serious Chronic Illnesses History', validators=[Optional()])

    head_injuries = BooleanField('Head Injuries', validators=[Optional()])
    lose_consciousness = BooleanField('Lose Consciousness', validators=[Optional()])
    convulsions_or_seizures = BooleanField('Convulsions or Seizures', validators=[Optional()])
    fever = BooleanField('Fever', validators=[Optional()])
    allergies = StringField('Allergies', validators=[Optional()])

    current_physical_health = StringField('Current Physical Health', validators=[Optional()])
    last_check_up = DateField('Last Check-Up', validators=[Optional()])
    has_physician = BooleanField('Has Physician', validators=[Optional()])
    physician_name = StringField('Physician Name', validators=[Optional()])
    physician_email = StringField('Physician Email', validators=[Optional()])
    physician_number = StringField('Physician Number', validators=[Optional()])

    # Family Background

    birth_location = StringField('Birth Location', validators=[Optional()])
    raised_by = StringField('Raised By', validators=[Optional()])

    rel_qual_mother = StringField('Relationship Quality with Mother', validators=[Optional()])
    rel_qual_father = StringField('Relationship Quality with Father', validators=[Optional()])
    rel_qual_step_parent = StringField('Relationship Quality with Step Parent', validators=[Optional()])

    family_abuse_history = StringField('Family Abuse History', validators=[Optional()])
    family_mental_history = StringField('Family Mental History', validators=[Optional()])
    additional_information_family = StringField('Additional Information', validators=[Optional()])

    # Social History
    relationship_with_peers = StringField('Relationship with Peers', validators=[Optional()])
    social_support_network = StringField('Social Support Network', validators=[Optional()])
    hobbies_or_interests = StringField('Hobbies or Interests', validators=[Optional()])
    cultural_concerns = StringField('Cultural Concerns', validators=[Optional()])

    # Educational Background
    educational_history = StringField('Educational History', validators=[Optional()])
    highest_level_achieved = StringField('Highest Level Achieved', validators=[Optional()])
    additional_information_education = StringField('Additional Information', validators=[Optional()])

    # Occupational History
    employment_status = StringField('Employment Status', validators=[Optional()])
    satisfaction = StringField('Satisfaction', validators=[Optional()])
    satisfaction_reason = StringField('Satisfaction Reason', validators=[Optional()])

    # Substance Abuse History
    struggled_with_substance_abuse = BooleanField('Struggled with Substance Abuse', validators=[Optional()])
    alcohol = BooleanField('Alcohol', validators=[Optional()])
    alcohol_age_first_use = StringField('Alcohol Age of First Use', validators=[Optional()])
    alcohol_frequency_of_use = StringField('Alcohol Frequency of Use', validators=[Optional()])
    alcohol_amount_used = StringField('Alcohol Amount Used', validators=[Optional()])
    alcohol_way_of_intake = StringField('Alcohol Way of Intake', validators=[Optional()])

    cigarette = BooleanField('Cigarette', validators=[Optional()])
    cigarette_age_first_use = StringField('Cigarette Age of First Use', validators=[Optional()])
    cigarette_frequency_of_use = StringField('Cigarette Frequency of Use', validators=[Optional()])
    cigarette_amount_used = StringField('Cigarette Amount Used', validators=[Optional()])
    cigarette_way_of_intake = StringField('Cigarette Way of Intake', validators=[Optional()])
    
    marijuana = BooleanField('Marijuana', validators=[Optional()])
    marijuana_age_first_use = StringField('Marijuana Age of First Use', validators=[Optional()])
    marijuana_frequency_of_use = StringField('Marijuana Frequency of Use', validators=[Optional()])
    marijuana_amount_used = StringField('Marijuana Amount Used', validators=[Optional()])
    marijuana_way_of_intake = StringField('Marijuana Way of Intake', validators=[Optional()])
    
    cocaine = BooleanField('Cocaine', validators=[Optional()])
    cocaine_age_first_use = StringField('Cocaine Age of First Use', validators=[Optional()])
    cocaine_frequency_of_use = StringField('Cocaine Frequency of Use', validators=[Optional()])
    cocaine_amount_used = StringField('Cocaine Amount Used', validators=[Optional()])
    cocaine_way_of_intake = StringField('Cocaine Way of Intake', validators=[Optional()])
    
    heroin = BooleanField('Heroin', validators=[Optional()])
    heroin_age_first_use = StringField('Heroin Age of First Use', validators=[Optional()])
    heroin_frequency_of_use = StringField('Heroin Frequency of Use', validators=[Optional()])
    heroin_amount_used = StringField('Heroin Amount Used', validators=[Optional()])
    heroin_way_of_intake = StringField('Heroin Way of Intake', validators=[Optional()])
    
    amphetamines = BooleanField('Amphetamines', validators=[Optional()])
    amphetamines_age_first_use = StringField('Amphetamines Age of First Use', validators=[Optional()])
    amphetamines_frequency_of_use = StringField('Amphetamines Frequency of Use', validators=[Optional()])
    amphetamines_amount_used = StringField('Amphetamines Amount Used', validators=[Optional()])
    amphetamines_way_of_intake = StringField('Amphetamines Way of Intake', validators=[Optional()])
    
    club_drugs = BooleanField('Club Drugs', validators=[Optional()])
    club_drugs_age_first_use = StringField('Club Drugs Age of First Use', validators=[Optional()])
    club_drugs_frequency_of_use = StringField('Club Drugs Frequency of Use', validators=[Optional()])
    club_drugs_amount_used = StringField('Club Drugs Amount Used', validators=[Optional()])
    club_drugs_way_of_intake = StringField('Club Drugs Way of Intake', validators=[Optional()])
    
    pain_meds = BooleanField('Pain Meds', validators=[Optional()])
    pain_meds_age_first_use = StringField('Pain Meds Age of First Use', validators=[Optional()])
    pain_meds_frequency_of_use = StringField('Pain Meds Frequency of Use', validators=[Optional()])
    pain_meds_amount_used = StringField('Pain Meds Amount Used', validators=[Optional()])
    pain_meds_way_of_intake = StringField('Pain Meds Way of Intake', validators=[Optional()])
    
    benzo = BooleanField('Benzodiazepines', validators=[Optional()])
    benzo_age_first_use = StringField('Benzodiazepines Age of First Use', validators=[Optional()])
    benzo_frequency_of_use = StringField('Benzodiazepines Frequency of Use', validators=[Optional()])
    benzo_amount_used = StringField('Benzodiazepines Amount Used', validators=[Optional()])
    benzo_way_of_intake = StringField('Benzodiazepines Way of Intake', validators=[Optional()])
    
    hallucinogens = BooleanField('Hallucinogens', validators=[Optional()])
    hallucinogens_age_first_use = StringField('Hallucinogens Age of First Use', validators=[Optional()])
    hallucinogens_frequency_of_use = StringField('Hallucinogens Frequency of Use', validators=[Optional()])
    hallucinogens_amount_used = StringField('Hallucinogens Amount Used', validators=[Optional()])
    hallucinogens_way_of_intake = StringField('Hallucinogens Way of Intake', validators=[Optional()])
    
    other_meds = BooleanField('Other', validators=[Optional()])
    other_meds_age_first_use = StringField('Other Age of First Use', validators=[Optional()])
    other_meds_frequency_of_use = StringField('Other Frequency of Use', validators=[Optional()])
    other_meds_amount_used = StringField('Other Amount Used', validators=[Optional()])
    other_meds_way_of_intake = StringField('Other Way of Intake', validators=[Optional()])


    # Legal History
    pending_criminal_charges = BooleanField('Pending Criminal Charges', validators=[Optional()])
    on_probation = BooleanField('On Probation', validators=[Optional()])
    has_been_arrested = BooleanField('Has Been Arrested', validators=[Optional()])

    # Additional Information
    to_work_on = StringField('To Work On', validators=[Optional()])
    expectations = StringField('Expectations', validators=[Optional()])
    things_to_change = StringField('Things to Change', validators=[Optional()])
    other_information = StringField('Other Information', validators=[Optional()])
