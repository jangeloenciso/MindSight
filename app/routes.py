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
from app.forms.upload import UploadFileForm
from functools import wraps
from werkzeug.utils import secure_filename
import logging, os
from datetime import datetime


SECURITY_QUESTIONS = {
            'question1': 'In what city did your parents meet?',
            'question2': 'Where did you go on your first solo trip?',
            'question3': 'What was the first dish you learned to cook?',
            'question4': 'What was the name of your first stuffed toy?',
            'question5': 'What was the title of the first book you read?'
}

ROLE = {
    'admin1': 'Director',
    'admin2': 'Head, Counseling and Wellness',
    'admin3': 'GCSC Personnel-Pasig',
    'admin4': 'Registered Psychometrician',
}



@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return jsonify({'success': True })
        
        else:
            flash('Login failed. Please check your username and password.', 'danger')
            print('User not found. Please check your username.', 'danger')
            return jsonify({'error': True })

    return render_template('login.html', form=form, current_user=current_user)


@app.route('/signup', methods=['POST', 'GET'])
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
@login_required
def admin():

    admin = User.query.all()

    for user in admin:
        user.full_name = user.first_name + ' ' + user.last_name
        user.role = ROLE.get(user.role, 'Unknown Role')

    return render_template('admin.html', admin=admin)


@app.route('/admin/history')
@login_required
def counseling_history():

    full_name = request.args.get('full_name', default='', type=str)

    return render_template('admin/counseling_history.html', full_name=full_name)



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
@login_required
def search():
    query = request.args.get('query')

    print(query)

    search_data = process_data(search_query=query)
    search_results = search_data.to_dict(orient='records')

    print(search_results)

    return render_template('search.html', search_results=search_results, query=query)

@app.route('/students/records/view/<student_id>/print')
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
@login_required
def level():
    return render_template('level.html')

@app.route('/JHS')
@login_required
def jhs():
    return render_template('jhs.html')

@app.route('/students/records/<college>')
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
@login_required
def shs():
    return render_template('shs.html')

@app.route('/students/records/<college>')
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
@login_required
def colleges():
    return render_template('colleges.html')

@app.route('/students/records/<college>')
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
@login_required
def graduate():
    return render_template('graduate.html')

@app.route('/students/records/<college>')
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
@login_required
def student_record(student_id):
    data = process_data(student_id)
    student_data = data.to_dict(orient='records')

    print(student_id)

    return render_template('students/student_record.html', student_id=student_id, student_data=student_data)

@app.route('/students/records/view/full_record/<student_id>', methods=['GET', 'POST'])
@login_required
def full_record(student_id):

    data = process_data(student_id)
    student_data = data.to_dict(orient='records')
    
    return render_template('students/full_record.html', student_id=student_id, student_data=student_data)


# Upload File
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'} 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/students/records/upload/<student_id>', methods=['GET', 'POST'])
def upload_file(student_id):
    app.logger.info(f"UPLOAD_FOLDER: {UPLOAD_FOLDER}")
    
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        destination = os.path.join(UPLOAD_FOLDER, filename)
        app.logger.info(f"Destination path: {destination}")

        os.makedirs(os.path.dirname(destination), exist_ok=True)
        file.save(destination)

        document = Document(filename=filename, path=destination, student_id=student_id)
        db.session.add(document)
        db.session.commit()

        flash('File uploaded successfully', 'success')
        return redirect(url_for('student_record', student_id=student_id))

    flash('Invalid file type', 'danger')
    return redirect(request.url)



# View uploaded file
@app.route('/get_uploaded_file_path/<student_id>')
def get_uploaded_file_path(student_id):

    # TODO: Ano to
    document = Document.query.filter_by(student_id=student_id).first()

    if document:
        file_url = url_for('upload_file', student_id=student_id)
        return jsonify({'file_url': file_url})
    
    else:
        return jsonify({'error': 'Document not found'}), 404



@app.route('/students/records/edit/<student_id>', methods=['GET', 'POST'])
@login_required
def edit_record(student_id):
    with db.session.no_autoflush:
        student = (
            BasicInformation.query
            .options(
                joinedload(BasicInformation.family_background),
                joinedload(BasicInformation.health_information),
                joinedload(BasicInformation.educational_background),
                joinedload(BasicInformation.social_history),
                joinedload(BasicInformation.history_information),
                joinedload(BasicInformation.occupational_history),
                joinedload(BasicInformation.substance_abuse_history),
                joinedload(BasicInformation.legal_history),
                joinedload(BasicInformation.additional_information),
                joinedload(BasicInformation.sessions),
                joinedload(BasicInformation.case_note)
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
            form.populate_obj(student.family_background)
            form.populate_obj(student.health_information)
            form.populate_obj(student.educational_background)
            form.populate_obj(student.social_history)
            form.populate_obj(student.history_information)
            form.populate_obj(student.occupational_history)
            form.populate_obj(student.substance_abuse_history)
            form.populate_obj(student.legal_history)
            form.populate_obj(student.additional_information)


            # TODO: Handle delete
            existing_siblings = student.family_background.siblings

            sibling_names = request.form.getlist('siblingName')
            sibling_ages = request.form.getlist('siblingAge')
            sibling_genders = request.form.getlist('siblingGender')
            sibling_rel_quals = request.form.getlist('rel_qual')

            for sibling_index, sibling_name in enumerate(sibling_names):
                if sibling_index < len(existing_siblings):
                    existing_sibling = existing_siblings[sibling_index]
                    existing_sibling.name = sibling_name
                    existing_sibling.age = sibling_ages[sibling_index]
                    existing_sibling.gender = sibling_genders[sibling_index]
                    existing_sibling.rel_qual = sibling_rel_quals[sibling_index]
                else:
                    if len(sibling_names) > 1:
                        new_sibling = Sibling(
                            name=sibling_name,
                            age=sibling_ages[sibling_index],
                            gender=sibling_genders[sibling_index],
                            rel_qual=sibling_rel_quals[sibling_index],
                            family_background=student.family_background
                        )
                        db.session.add(new_sibling)

            existing_convictions = student.legal_history.convictions
            

            convictions = request.form.getlist('legalConviction')
            conviction_dates = request.form.getlist('legalDate')
            conviction_outcomes = request.form.getlist('legalOutcome')
            
            for conviction_index, conviction in enumerate(convictions):
                if conviction_index < len(existing_convictions):
                    existing_conviction = existing_convictions[conviction_index]
                    existing_conviction.conviction = conviction
                    existing_conviction.conviction_date = conviction_dates[conviction_index]
                    existing_conviction.conviction_outcome = conviction_outcomes[conviction_index]
                else:
                    if len(convictions) >= 1:
                        new_conviction = Conviction(
                            conviction=conviction,
                            conviction_date=conviction_dates[conviction_index],
                            conviction_outcome=conviction_outcomes[conviction_index],
                            legal_history=student.legal_history
                        )
                        db.session.add(new_conviction)
        
            counselor_list = request.form.getlist('counselorName')
            interview_date = request.form.getlist('interviewDate')
            number_of_session = request.form.getlist('numberOfSession')
            subject_complaint = request.form.getlist('subjectComplaint')
            objective_assessment = request.form.getlist('objectiveAssessment')
            plan_of_action = request.form.getlist('planOfAction')
            progress_made = request.form.getlist('progressMade')

            if any(counselor_list) or any(interview_date) or any(number_of_session) or any(subject_complaint) or any(objective_assessment) or any(plan_of_action) or any(progress_made):
                for case_note in range(len(counselor_list)):
                    if len(counselor_list) >= 1:
                        new_case_note = CaseNote(
                            counselor_name = counselor_list[case_note],
                            interview_date = interview_date[case_note],
                            number_of_session = number_of_session[case_note],
                            subject_complaint = subject_complaint[case_note],
                            objective_assessment = objective_assessment[case_note],
                            plan_of_action = plan_of_action[case_note],
                            progress_made = progress_made[case_note],
                            student_id=student.student_id
                        )
                        db.session.add(new_case_note)

            session_date = request.form.getlist('sessionDate')
            session_time_start = request.form.getlist('sessionTimeStart')
            session_time_end = request.form.getlist('sessionTimeEnd')
            session_follow_up = request.form.getlist('sessionFollowUp')
            session_attended_by = request.form.getlist('sessionAttendedBy')

            print(len(session_date))
            
            # EXTREMELY BAD PRACTICE BUT IM TOO TIRED
            for session in student.sessions:
                db.session.delete(session)

            for session in range(len(session_date)):
                print("SESSIONS")
                new_session = Sessions(
                    session_date = session_date[session],
                    session_time_start=session_time_start[session],
                    session_time_end=session_time_end[session],
                    session_follow_up=session_follow_up[session],
                    session_attended_by=session_attended_by[session],
                    student_id=student.student_id
                )
                if new_session not in student.sessions:
                    print(new_session)
                    db.session.add(new_session)

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
            nature_of_concern=request.form.get('nature_of_concern'),
            counselor=form.counselor.data,
            personal_agreement=form.personal_agreement.data,
            personal_agreement_date=form.personal_agreement_date.data,

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

        # referral_information = ReferralInformation(
        #     reason_for_referral=form.reason_for_referral.data,
        #     receiving_agency=form.receiving_agency.data,
        #     receiving_contact_number=form.receiving_contact_number.data,
        #     receiving_name=form.receiving_name.data,
        #     receiving_email=form.receiving_email.data,
        #     office_address=form.office_address.data,
        #     appointment_schedule=form.appointment_schedule.data,
            
        #     client_signature=form.client_signature.data,
        #     counselor_signature=form.counselor_signature.data,
        # )

        # case_note = CaseNote(
        #     counselor_name=form.counselor_name.data,
        #     interview_date=request.form.get('confiinterview'),
        #     number_of_session=form.number_of_session.data,

        #     subject_complaint=form.subject_complaint.data,
        #     objective_assessment=form.objective_assessment.data,
        #     plan_of_action=form.plan_of_action.data,
        #     progress_made=form.progress_made.data
        # )

        new_student = BasicInformation(
            student_id=form.student_id.data,
            last_name=form.last_name.data,
            first_name=form.first_name.data,
            college=request.form.get('college'),
            course=request.form.get('course'),
            year_level=request.form.get('year_level'),
            campus=request.form.get('campus'),
            guardian_name = form.guardian_name.data,
            guardian_address = form.guardian_address.data,
            guardian_contact = form.guardian_contact.data,

            date_of_birth = request.form.get('date_of_birth'),
            age = form.age.data,
            gender = request.form.get('gender'),
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
            # referral_information=referral_information,
            # case_note=case_note
        )



        # Add the new records to the database
        db.session.add(new_student)

        sibling_names = request.form.getlist('siblingName')
        sibling_ages = request.form.getlist('siblingAge')
        sibling_genders = request.form.getlist('siblingGender')
        sibling_rel_quals = request.form.getlist('rel_qual')

        # This entire block of code is bad
        if len(sibling_names) > 1:
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

        # This entire block of code is bad
        if len(convictions) > 1:
            for conviction in range(len(convictions)):
                new_conviction = Conviction(
                    conviction = convictions[conviction],
                    conviction_date = conviction_dates[conviction],
                    conviction_outcome = conviction_outcomes[conviction],
                    legal_history = legal_history
                )
                db.session.add(new_conviction)


        db.session.commit()

        # Flash a success message
        flash('New student record added successfully!', 'success')

        print(new_student.student_id)

        # Redirect the user to a page displaying the newly added record
        # return redirect(url_for('student_record', new_record_id=new_student.id))
        return jsonify({'success': True})
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
