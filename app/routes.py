from app import app, db, bcrypt
from app.models.models import *
from sqlalchemy.orm import joinedload
from flask import render_template, url_for, redirect, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from .data_processing import *
from .forms import *
from flask_login import login_user
from app.forms.signup import SignupForm
from app.forms.login import LoginForm
from app.forms.student_record import StudentRecordForm
from app.forms.edit_credentials import EditCredentials
from app.forms.forgot import ForgotPassword
from app.forms.reset import ResetPassword
from functools import wraps
import logging, datetime


roles_permissions = {
    'admin': ['view', 'edit', 'search', 'delete']
}

SECURITY_QUESTIONS = {
            'question1': 'In what city did your parents meet?',
            'question2': 'Where did you go on your first solo trip?',
            'question3': 'What was the first dish you learned to cook?',
            'question4': 'What was the name of your first stuffed toy?',
            'question5': 'What was the title of the first book you read?'
}

def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if current user has the required permission
            user_role = getattr(current_user, 'role', None)
            if user_role == 'superadmin':
                return func(*args, **kwargs)

            if user_role in roles_permissions and permission in roles_permissions[user_role]:
                return func(*args, **kwargs)
            else:
                print('You do not have permission to access this page.', 'danger')
                return redirect(url_for('dashboard'))
        return wrapper
    return decorator


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        
        else:
            flash('Login failed. Please check your username and password.', 'danger')
            print('User not found. Please check your username.', 'danger')

    return render_template('login.html', form=form, current_user=current_user)


@app.route('/signup', methods=['POST', 'GET'])
# @permission_required('create_account')
def signup():

    form = SignupForm()

    if form.validate_on_submit(): 

        _username = form.username.data
        _password = form.password.data
        _email = form.email.data
        _role = form.role.data
        _security_question = form.security_question.data
        _security_answer = form.security_answer.data

        user = User.query.filter_by(username=_username).first()
        if user:
            prmpt = f'Sorry, but the username "{_username}" is already taken'
            prmpt = f'Sorry, but the username "{_email}" is already taken'
        else:
            hashed_password = bcrypt.generate_password_hash(_password).decode('utf-8')
            hashed_security_answer = bcrypt.generate_password_hash(_security_answer).decode('utf-8')
            new_user = User( first_name=form.first_name.data, 
                             last_name=form.last_name.data, 
                             username=_username, 
                             email=form.email.data, 
                             password=hashed_password, 
                             role=_role, 
                             security_question=_security_question, 
                             security_answer=hashed_security_answer )
            
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)

            return jsonify({'success': True})
    else:
        prmpt = 'Please correct the form errors.'

    return render_template('signup.html', form=form, prmpt=prmpt)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# TODO: Accessible directly through the URL. Enhance security
@app.route('/forgot-password', methods=['POST', 'GET'])
def forgot_password():
    form = ForgotPassword()

    if form.validate_on_submit():
        _username = form.username.data
        user = User.query.filter_by(username=_username).first()
        
        if user:
            return jsonify({'success': True})
        
        else:
            print('User does not exist.', 'error')
            return jsonify({'error': True})
    
    return render_template('forgot.html', form=form)

# TODO: Accessible directly through the URL. Enhance security
@app.route('/reset-password/<username>', methods=['POST', 'GET'])
def reset_password(username):

    form = ResetPassword()

    user = User.query.filter_by(username=username).first()

    if not user:
        flash('User not found', 'error')
        return redirect(url_for('login'))
    
    if form.validate_on_submit():

        if bcrypt.check_password_hash(user.security_answer, form.security_answer.data):
            new_password = form.password.data
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            user.password = hashed_password

            # Commit changes to the database
            db.session.commit()
            return jsonify({'success': True})
    
        else:
            print('Incorrect security answer.')
            return jsonify({'error': True})
    
    _security_question = user.security_question
    security_question = SECURITY_QUESTIONS.get(_security_question, 'Unknown Question')

    return render_template('reset.html', form=form, security_question=security_question, username=username)

# Pages

# for dashboard / case overview pages
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard/experiences', methods=['GET'])
@login_required
def experiences():
    
    return render_template('dashboard/experiences.html')

@app.route('/dashboard/college_summary', methods=['GET'])
@login_required
def college_summaries():
    
    return render_template('dashboard/college_summaries.html')

@app.route('/dashboard/nature_of_concern', methods=['GET'])
@login_required
def nature_of_concern():
    
    return render_template('dashboard/nature_concern.html')

@app.route('/dashboard/campus', methods=['GET'])
@login_required
def campus():
    
    return render_template('dashboard/campus.html')

@app.route('/dashboard/religion', methods=['GET'])
@login_required
def religion():
    
    return render_template('dashboard/religion.html')

@app.route('/dashboard/identity', methods=['GET'])
@login_required
def identity():
    
    return render_template('dashboard/identity.html')


# pages for admin / viewing of students whose been counseled
@app.route('/admin')
@permission_required('view')
@login_required
def admin():

    counselors = ['Emmanuelle Santiago',
                  'Russel Ane Dela Cruz', 
                  'Jake Jason Queddeng', 
                  'Lizelle Anne Manabat']    


    counselor_titles = ['Director',
                        'Head, Counseling and Wellness',
                        'GCSC Personnel-Pasig',
                        'Registered Psychometrician']
    
    counselor_data = zip(counselors, counselor_titles) 
    user_name = current_user.first_name + ' ' + current_user.last_name

    # if superadmin, can access all buttons/files
    if current_user.role == 'superadmin':
        user_counselor_data = counselor_data
    
    # if admin, can only access their own button/file
    else:
        user_counselor_data = [(counselor, title) for counselor, title in counselor_data if counselor == user_name]

    return render_template('admin.html', user_counselor_data=user_counselor_data)

@app.route('/admin/history')
@permission_required('view')
@login_required
def counseling_history():

    counselor_name = request.args.get('counselor_name', default='', type=str)

    return render_template('admin/counseling_history.html', counselor_name=counselor_name)



# analytics
@app.route('/analytics', methods=['GET', 'POST'])
@login_required
def analytics():
    return render_template('analytics.html')

@app.route('/analytics/analysis')
@login_required
def metrics():
    return render_template('metrics.html')


# settings page
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():

    form = EditCredentials(request.form)


    if form.validate_on_submit():
        if not bcrypt.check_password_hash(current_user.password, form.current_password.data):
            flash('Incorrect password. Please try again.', 'danger')
            return redirect(url_for('settings'))
        
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.confirm = form.confirm.data

        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password

        # Commit changes to the database
        db.session.commit()
        return jsonify({'success': True})


    return render_template('settings.html', form=form)


@app.route('/students/records/search/', methods=['GET'])
@permission_required('search')
@login_required
def search():
    query = request.args.get('query')

    print(query)

    search_data = process_data(search_query=query)
    search_results = search_data.to_dict(orient='records')

    print(search_results)

    return render_template('search.html', search_results=search_results, query=query)

@app.route('/students/records/view/<student_id>/print')
@permission_required('print')
@login_required
def print_record(student_id):
    data = process_data(student_id)
    student_data = data.to_dict(orient='records')

    print(student_id)

    if len(student_data) == 0:
        # TODO: ADD A FLASH "STUDENT NOT FOUND"
        print("mayo amp")
        return redirect(url_for('students'))

    return render_template('print_record.html', student_data=student_data)


# Student components

@app.route('/level')
@permission_required('view')
@login_required
def level():
    return render_template('level.html')

@app.route('/JHS')
@permission_required('view')
@login_required
def jhs():
    return render_template('jhs.html')

@app.route('/students/records/<college>')
@permission_required('view')
@login_required
def jhs_records(college):
    data = data_to_dict()

    def college_name(college):
        college_dict = {
            'SEVEN': 'Grade 7',
            'EIGHT': 'Grade 8',
            'NINE': 'Grade 9',
            'TEN': 'Grade 10',
        }
        return college_dict.get(college)

    print(college_name(college))

    return render_template('students/records.html', college_name=college_name(college), college=college, data=data)

@app.route('/SHS')
@permission_required('view')
@login_required
def shs():
    return render_template('shs.html')

@app.route('/students/records/<college>')
@permission_required('view')
@login_required
def shs_records(college):
    data = data_to_dict()

    def college_name(college):
        college_dict = {
            'STEM': 'Science, Technology, Engineering and Mathematics',
            'ABM': 'Accountancy, Business and Management',
            'HUMSS': 'Humanities and Social Sciences',
            'ICT': 'Information Communication and Technology',
        }
        return college_dict.get(college)

    print(college_name(college))

    return render_template('students/records.html', college_name=college_name(college), college=college, data=data)

@app.route('/colleges')
@permission_required('view')
@login_required
def colleges():
    return render_template('colleges.html')

@app.route('/students/records/<college>')
@permission_required('view')
@login_required
def college_records(college):
    data = data_to_dict()

    def college_name(college):
        college_dict = {
            'CEA': 'College of Engineering and Architecture',
            'CBEA': 'College of Business Entrepreneurship and Accountancy',
            'CAS': 'College of Arts and Sciences',
            'CED': 'College of Education',
            'IHK': 'Institute of Human Kinetics',
        }
        return college_dict.get(college)

    print(college_name(college))

    return render_template('students/records.html', college_name=college_name(college), college=college, data=data)

@app.route('/graduate')
@permission_required('view')
@login_required
def graduate():
    return render_template('graduate.html')

@app.route('/students/records/<college>')
@permission_required('view')
@login_required
def graduate_records(college):
    data = data_to_dict()

    def college_name(college):
        college_dict = {
            'GRAD': 'Graduate',
        }
        return college_dict.get(college)

    print(college_name(college))

    return render_template('students/records.html', college_name=college_name(college), college=college, data=data)

@app.route('/students/records/view/<student_id>')
@permission_required('view')
@login_required
def student_record(student_id):
    data = process_data(student_id)
    student_data = data.to_dict(orient='records')

    print(student_id)

    return render_template('students/student_record.html', student_data=student_data)


@app.route('/students/records/edit/<student_id>', methods=['GET', 'POST'])
@permission_required('edit')
@login_required
def edit_record(student_id):
    student = (
        BasicInformation.query
        .options(
            joinedload(BasicInformation.personal_information),
            joinedload(BasicInformation.family_background),
            joinedload(BasicInformation.health_information),
            joinedload(BasicInformation.educational_background),
            joinedload(BasicInformation.social_history),
            joinedload(BasicInformation.history_information),
            joinedload(BasicInformation.occupational_history),
            joinedload(BasicInformation.substance_abuse_history),
            joinedload(BasicInformation.legal_history),
            joinedload(BasicInformation.additional_information)
        )
        .filter_by(student_id=student_id)
        .first()
    )
    
    # if not student:
    #     flash('Student not found', 'danger')
    #     return redirect(url_for('college_records', college="CBEA"))

    form = StudentRecordForm(obj=student)

    if form.validate_on_submit():
        print('validated')
        form.populate_obj(student)
        form.populate_obj(student.personal_information)
        form.populate_obj(student.family_background)
        form.populate_obj(student.health_information)
        form.populate_obj(student.educational_background)
        form.populate_obj(student.social_history)
        form.populate_obj(student.history_information)
        form.populate_obj(student.occupational_history)
        form.populate_obj(student.substance_abuse_history)
        form.populate_obj(student.legal_history)
        form.populate_obj(student.additional_information)

        db.session.commit()
        print('Student record updated successfully', 'success')
        return redirect(url_for('student_record', student_id=student_id))
    
    print(form.errors)

    return render_template('students/edit_record.html', form=form, student_id=student_id, student=student)


@app.route('/add', methods=['GET', 'POST'])
def add_record():
    form = StudentRecordForm()

    if form.validate_on_submit():
        history_info = HistoryInformation(
            # -- DONE: verified 'other' field --works.
            # TODO: Frontend, remove/disable checkbox for other
            information_provider=request.form.get('information_provider'),

            current_problem=form.current_problem.data,
            problem_length=form.problem_length.data,

            stressors=form.stressors.data,

            substance_abuse=form.substance_abuse.data,
            addiction=form.addiction.data,
            depression_sad_down_feelings=form.depression_sad_down_feelings.data,
            high_low_energy_level=form.high_low_energy_level.data,
            angry_irritable=form.angry_irritable.data,
            loss_of_interest=form.loss_of_interest.data,
            difficulty_enjoying_things=form.difficulty_enjoying_things.data,
            crying_spells=form.crying_spells.data,
            decreased_motivation=form.decreased_motivation.data,
            withdrawing_from_people=form.withdrawing_from_people.data,
            mood_swings=form.mood_swings.data,
            black_and_white_thinking=form.black_and_white_thinking.data,
            negative_thinking=form.negative_thinking.data,
            change_in_weight_or_appetite=form.change_in_weight_or_appetite.data,
            change_in_sleeping_pattern=form.change_in_sleeping_pattern.data,
            suicidal_thoughts_or_plans=form.suicidal_thoughts_or_plans.data,
            self_harm=form.self_harm.data,
            homicidal_thoughts_or_plans=form.homicidal_thoughts_or_plans.data,
            difficulty_focusing=form.difficulty_focusing.data,
            feelings_of_hopelessness=form.feelings_of_hopelessness.data,
            feelings_of_shame_or_guilt=form.feelings_of_shame_or_guilt.data,
            feelings_of_inadequacy=form.feelings_of_inadequacy.data,
            
            # TODO: Done --Refactor, magkaibahan si inadequacy tas self-esteem
            anxious_nervous_tense_feelings=form.anxious_nervous_tense_feelings.data,
            panic_attacks=form.panic_attacks.data,
            racing_or_scrambled_thoughts=form.racing_or_scrambled_thoughts.data,
            bad_or_unwanted_thoughts=form.bad_or_unwanted_thoughts.data,
            flashbacks_or_nightmares=form.flashbacks_or_nightmares.data,
            muscle_tensions_aches=form.muscle_tensions_aches.data,
            hearing_voices_or_seeing_things=form.hearing_voices_or_seeing_things.data,
            thoughts_of_running_away=form.thoughts_of_running_away.data,
            paranoid_thoughts=form.paranoid_thoughts.data,
            feelings_of_frustration=form.feelings_of_frustration.data,
            feelings_of_being_cheated=form.feelings_of_being_cheated.data,
            perfectionism=form.perfectionism.data,
            counting_washing_checking=form.counting_washing_checking.data,
            distorted_body_image=form.distorted_body_image.data,
            concerns_about_dieting=form.concerns_about_dieting.data,
            loss_of_control_over_eating=form.loss_of_control_over_eating.data,
            binge_eating_or_purging=form.binge_eating_or_purging.data,
            rules_about_eating=form.rules_about_eating.data,
            compensating_for_eating=form.compensating_for_eating.data,
            excessive_exercise=form.excessive_exercise.data,
            indecisiveness_about_career=form.indecisiveness_about_career.data,
            job_problems=form.job_problems.data,

            # TODO: DONE --verified works
            other=form.other_history.data,

            # TODO: DONE --verified works
            previous_treatments=form.previous_treatments.data,

            previous_treatments_likes_dislikes=form.previous_treatments_likes_dislikes.data,
            previous_treatments_learned=form.previous_treatments_learned.data,
            previous_treatments_like_to_continue=form.previous_treatments_like_to_continue.data,
            previous_hospital_stays_psych=form.previous_hospital_stays_psych.data,
            current_thoughts_to_harm=form.current_thoughts_to_harm.data,
            past_thoughts_to_harm=form.past_thoughts_to_harm.data,
            student_id=form.student_id.data
        )

        # TODO: DONE --verified working all
        health_info = HealthInformation(
            medication_and_dose=form.medication_and_dose.data,

            serious_ch_illnesses_history=form.serious_ch_illnesses_history.data,

            head_injuries=form.head_injuries.data,
            lose_consciousness=form.lose_consciousness.data,
            convulsions_or_seizures=form.convulsions_or_seizures.data,
            fever=form.fever.data,
            allergies=form.allergies.data,

            current_physical_health=form.current_physical_health.data,
            last_check_up=form.last_check_up.data,
            has_physician=form.has_physician.data,
            physician_name=form.physician_name.data,
            physician_email=form.physician_email.data,
            physician_number=form.physician_number.data,

            student_id=form.student_id.data
        )

        family_background = FamilyBackground(
            birth_location = form.birth_location.data,
            raised_by = form.raised_by.data,
            
            # TODO: add an other field --done, added field
            rel_qual_mother = form.rel_qual_mother.data,
            rel_qual_father = form.rel_qual_father.data,
            rel_qual_step_parent = form.rel_qual_step_parent.data,
            rel_qual_other = form.rel_qual_other.data,

            # TODO: add siblings and shit

            family_abuse_history=form.family_abuse_history.data,
            family_mental_history=form.family_mental_history.data,
            additional_information=form.additional_information_family.data,

            # siblings = siblings,

            student_id=form.student_id.data
        )

        social_history = SocialHistory(
            relationship_with_peers=form.relationship_with_peers.data,
            social_support_network=form.social_support_network.data,
            hobbies_or_interests=form.hobbies_or_interests.data,
            cultural_concerns=form.cultural_concerns.data,
            student_id=form.student_id.data
        )

        educational_background = EducationalBackground(
            educational_history=form.educational_history.data,
            highest_level_achieved=form.highest_level_achieved.data,
            additional_information=form.additional_information_education.data,
            student_id=form.student_id.data
        )

        
        # TODO: Increase max length for fields
        occupational_history = OccupationalHistory(
            employment_status=form.employment_status.data,
            satisfaction=form.satisfaction.data,
            satisfaction_reason=form.satisfaction_reason.data,
            student_id=form.student_id.data
        )

        substance_abuse_history = SubstanceAbuseHistory(
            struggled_with_substance_abuse=form.struggled_with_substance_abuse.data,
            # TODO: add other

            alcohol=request.form.get('alcoholuse'),
            alcohol_age_first_use=form.alcohol_age_first_use.data,
            alcohol_frequency_of_use=request.form.get('alcoholfrequency'),
            alcohol_amount_used=form.alcohol_amount_used.data,
            alcohol_way_of_intake=form.alcohol_way_of_intake.data,

            cigarette=request.form.get('cigaretteuse'),
            cigarette_age_first_use=form.cigarette_age_first_use.data,
            cigarette_frequency_of_use=request.form.get('cigarettefrequency'),
            cigarette_amount_used=form.cigarette_amount_used.data,
            cigarette_way_of_intake=form.cigarette_way_of_intake.data,
            
            marijuana=request.form.get('marijuanause'),
            marijuana_age_first_use=form.marijuana_age_first_use.data,
            marijuana_frequency_of_use=request.form.get('marijuanafrequency'),
            marijuana_amount_used=form.marijuana_amount_used.data,
            marijuana_way_of_intake=form.marijuana_way_of_intake.data,

            cocaine=request.form.get('cocaineorcrackuse'),
            cocaine_age_first_use=form.cocaine_age_first_use.data,
            cocaine_frequency_of_use=request.form.get('cocaineorcrackfrequency'),
            cocaine_amount_used=form.cocaine_amount_used.data,
            cocaine_way_of_intake=form.cocaine_way_of_intake.data,

            heroin=request.form.get('heroinuse'),
            heroin_age_first_use=form.heroin_age_first_use.data,
            heroin_frequency_of_use=request.form.get('heroinfrequency'),
            heroin_amount_used=form.heroin_amount_used.data,
            heroin_way_of_intake=form.heroin_way_of_intake.data,

            amphetamines=request.form.get('amphetaminesuse'),
            amphetamines_age_first_use=form.amphetamines_age_first_use.data,
            amphetamines_frequency_of_use=request.form.get('amphetaminesfrequency'),
            amphetamines_amount_used=form.amphetamines_amount_used.data,
            amphetamines_way_of_intake=form.amphetamines_way_of_intake.data,

            club_drugs=request.form.get('clubdrugsuse'),
            club_drugs_age_first_use=form.club_drugs_age_first_use.data,
            club_drugs_frequency_of_use=request.form.get('clubdrugsfrequency'),
            club_drugs_amount_used=form.club_drugs_amount_used.data,
            club_drugs_way_of_intake=form.club_drugs_way_of_intake.data,

            pain_meds=request.form.get('painmedicationuse'),
            pain_meds_age_first_use=form.pain_meds_age_first_use.data,
            pain_meds_frequency_of_use=request.form.get('painmedicationfrequency'),
            pain_meds_amount_used=form.pain_meds_amount_used.data,
            pain_meds_way_of_intake=form.pain_meds_way_of_intake.data,

            benzo=request.form.get('benzodiazepinesuse'),
            benzo_age_first_use=form.benzo_age_first_use.data,
            benzo_frequency_of_use=request.form.get('benzodiazepinesfrequency'),
            benzo_amount_used=form.benzo_amount_used.data,
            benzo_way_of_intake=form.benzo_way_of_intake.data,


            hallucinogens=request.form.get('hallucinogensuse'),
            hallucinogens_age_first_use=form.hallucinogens_age_first_use.data,
            hallucinogens_frequency_of_use=request.form.get('hallucinogensfrequency'),
            hallucinogens_amount_used=form.hallucinogens_amount_used.data,
            hallucinogens_way_of_intake=form.hallucinogens_way_of_intake.data,


            other_meds=form.other_meds.data,
            other_meds_age_first_use=form.other_meds_age_first_use.data,
            other_meds_frequency_of_use=request.form.get('otherfrequency'),
            other_meds_amount_used=form.other_meds_amount_used.data,
            other_meds_way_of_intake=form.other_meds_way_of_intake.data,

            treatment_program_name = form.treatment_program_name.data,
            treatment_type = form.treatment_type.data,
            treatment_date = form.treatment_date.data,
            treatment_outcome = form.treatment_outcome.data,

            student_id=form.student_id.data
        )

        legal_history = LegalHistory(
            pending_criminal_charges=form.pending_criminal_charges.data,
            on_probation=form.on_probation.data,
            has_been_arrested=form.has_been_arrested.data,

            student_id=form.student_id.data
        )

        additional_info = AdditionalInformation(
            nature_of_concern=form.nature_of_concern.data,
            counselor=form.counselor.data,
            personal_agreement=form.personal_agreement.data,

            referral_source = form.referral_source.data,

            emergency_name=form.emergency_name.data,
            emergency_relationship=form.emergency_relationship.data,
            emergency_address=form.emergency_address.data,
            emergency_contact=form.emergency_contact.data,
            
            to_work_on=form.to_work_on.data,
            expectations=form.expectations.data,
            things_to_change=form.things_to_change.data,
            other_information=form.other_information.data,


            student_id=form.student_id.data
        )

        referral_information = ReferralInformation(
            reason_for_referral=form.reason_for_referral.data,
            receiving_agency=form.receiving_agency.data,
            receiving_contact_number=form.receiving_contact_number.data,
            receiving_name=form.receiving_name.data,
            receiving_email=form.receiving_email.data,
            office_address=form.office_address.data,
            appointment_schedule=request.form.get('appointment_schedule'),
            
            client_signature=form.client_signature.data,
            counselor_signature=form.counselor_signature.data,
        )

        case_note = CaseNote(
            counselor_name=form.counselor_name.data,
            interview_date=request.form.get('confiinterview'),
            number_of_session=form.number_of_session.data,

            subject_complaint=form.subject_complaint.data,
            objective_assessment=form.objective_assessment.data,
            plan_of_action=form.plan_of_action.data,
            progress_made=form.progress_made.data
        )

        new_student = BasicInformation(
            student_id=form.student_id.data,
            last_name=form.last_name.data,
            first_name=form.first_name.data,
            course=form.course.data,
            year_level=form.year_level.data,
            campus=form.campus.data,
            guardian_name = form.guardian_name.data,
            guardian_address = form.guardian_address.data,
            guardian_contact = form.guardian_contact.data,
            

            date_of_birth = request.form.get('date_of_birth'),
            age = form.age.data,
            gender = form.gender.data,
            civil_status = request.form.get('civil'),
            nationality = form.nationality.data,
            religion = form.religion.data,
            residence = form.residence.data,
            contact_number = form.contact_number.data,
            phone_number = form.phone_number.data,
            email_address = form.email_address.data,

            history_information=history_info,
            health_information=health_info,
            family_background=family_background,
            social_history=social_history,
            educational_background=educational_background,
            occupational_history=occupational_history,
            substance_abuse_history=substance_abuse_history,
            legal_history=legal_history,
            additional_information=additional_info,
            referral_information=referral_information,
            case_note=case_note
        )

        print(request.form.get('date_of_birth') + "checking spaces")
        # print(sibling_names)

        # Add the new records to the database
        db.session.add(new_student)

        sibling_names = request.form.getlist('siblingName')
        sibling_ages = request.form.getlist('siblingAge')
        sibling_genders = request.form.getlist('siblingGender')
        sibling_rel_quals = request.form.getlist('rel_qual')

        # Iterating through sibling_names is VERY BAD PRACTICE. will refactor in the future.
        for sibling in range(len(sibling_names)):
            new_sibling = Sibling(
                name = sibling_names[sibling],
                age = sibling_ages[sibling],
                gender = sibling_genders[sibling],
                rel_qual = sibling_rel_quals[sibling],
                family_background=family_background
            )
            print(new_sibling.name)
            db.session.add(new_sibling)

        convictions = request.form.getlist('legalConviction')
        conviction_dates = request.form.getlist('legalDate')
        conviction_outcomes = request.form.getlist('legalOutcome')

        for conviction in range(len(convictions)):
            new_conviction = Conviction(
                conviction = convictions[conviction],
                conviction_date = conviction_dates[conviction],
                conviction_outcome = conviction_outcomes[conviction],
                legal_history = legal_history
            )
            db.session.add(new_conviction)

        print(sibling_names)

        db.session.commit()

        # Flash a success message
        flash('New student record added successfully!', 'success')

        print(new_student.student_id)

        # Redirect the user to a page displaying the newly added record
        # return redirect(url_for('student_record', new_record_id=new_student.id))
        return redirect(url_for('login'))
    else:
        logging.error("Form validation failed")
        logging.error(form.errors)

    # If the form is not submitted or not validated, or if it's a GET request, render the add record template
    return render_template('add_record.html', form=form)



# API endpoints

@app.route('/get_data/<first_metric>/<second_metric>', methods=['GET'])
def get_data(first_metric, second_metric):
    data = data_analytics(first_metric, second_metric)
    print(data)
    return jsonify(data)

@app.route('/get_data/<data_to_count>', methods=['GET'])
def get_college_count(data_to_count):
    data = data_count(data_to_count)
    print(data)
    return jsonify(data)
