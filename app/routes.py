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
# from app.forms.edit_record import EditStudentForm
# from app.forms.add_record import AddStudentForm
from app.forms.student_record import StudentRecordForm
from app.forms.edit_credentials import EditCredentials
from functools import wraps
import logging


roles_permissions = {
    'superadmin': ['viewall', 'editall', 'searchall', 'deleteall', 'addall'],
    'admin': ['viewall', 'view', 'editall','edit', 'search', 'delete', 'addall']
}

users = {
    'user1': 'superadmin',
    'user2': 'admin'
}

def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if current user has the required permission
            user_role = getattr(current_user, 'role', None)
            if user_role in roles_permissions and permission in roles_permissions[user_role]:
                return func(*args, **kwargs)
            else:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('dashboard'))
        return wrapper
    return decorator


@app.context_processor
def inject_role():
    role = getattr(current_user, 'role', None)
    return dict(role=role) 

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

    return render_template('login.html', form=form, current_user=current_user)


@app.route('/signup', methods=['POST', 'GET'])
def signup():

    form = SignupForm()

    if form.validate_on_submit(): 

        _username = form.username.data
        _password = form.password.data
        _email = form.email.data
        _role = form.role.data

        user = User.query.filter_by(username=_username).first()
        if user:
            prmpt = f'Sorry, but the username "{_username}" is already taken'
            prmpt = f'Sorry, but the username "{_email}" is already taken'
        else:
            hashed_password = bcrypt.generate_password_hash(_password).decode('utf-8')
            new_user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=_username, email=form.email.data, password=hashed_password, role=_role)
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


# Pages

# for dashboard / case overview pages
@app.route('/dashboard')
@permission_required('viewall')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard/experiences', methods=['GET'])
@permission_required('viewall')
@login_required
def experiences():
    
    return render_template('dashboard/experiences.html')

@app.route('/dashboard/college_summary', methods=['GET'])
@permission_required('viewall')
@login_required
def college_summaries():
    
    return render_template('dashboard/college_summaries.html')

@app.route('/dashboard/nature_of_concern', methods=['GET'])
@permission_required('viewall')
@login_required
def nature_of_concern():
    
    return render_template('dashboard/nature_concern.html')

@app.route('/dashboard/campus', methods=['GET'])
@permission_required('viewall')
@login_required
def campus():
    
    return render_template('dashboard/campus.html')

@app.route('/dashboard/religion', methods=['GET'])
@permission_required('viewall')
@login_required
def religion():
    
    return render_template('dashboard/religion.html')

@app.route('/dashboard/identity', methods=['GET'])
@permission_required('viewall')
@login_required
def identity():
    
    return render_template('dashboard/identity.html')


# pages for admin / viewing of students whose been counseled
@app.route('/admin')
@permission_required('viewall')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/admin/counselor')
@login_required
def counselor():
    return render_template('admin/college.html')

@app.route('/admin/counselor/counseling_history')
@login_required
def counseling_history():
    return render_template('admin/counseling_history.html')



@app.route('/analytics', methods=['GET', 'POST'])
@permission_required('viewall')
@login_required
def analytics():
    return render_template('analytics.html')

@app.route('/analytics/analysis')
@permission_required('viewall')
@login_required
def metrics():
    return render_template('metrics.html')


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
@permission_required('viewall')
@login_required
def search():
    query = request.args.get('query')

    print(query)

    search_data = process_data(search_query=query)
    search_results = search_data.to_dict(orient='records')

    print(search_results)

    return render_template('search.html', search_results=search_results, query=query)

@app.route('/students/records/view/<student_id>/print')
@permission_required('viewall')
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
@permission_required('viewall')
@login_required
def level():
    return render_template('level.html')

@app.route('/JHS')
@permission_required('viewall')
@login_required
def jhs():
    return render_template('jhs.html')

@app.route('/students/records/<college>')
@permission_required('viewall')
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
@permission_required('viewall')
@login_required
def shs():
    return render_template('shs.html')

@app.route('/students/records/<college>')
@permission_required('viewall')
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
@permission_required('viewall')
@login_required
def colleges():
    return render_template('colleges.html')

@app.route('/students/records/<college>')
@permission_required('viewall')
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
@permission_required('viewall')
@login_required
def graduate():
    return render_template('graduate.html')

@app.route('/students/records/<college>')
@permission_required('viewall')
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
@permission_required('viewall')
@login_required
def student_record(student_id):
    data = process_data(student_id)
    student_data = data.to_dict(orient='records')

    print(student_id)

    return render_template('students/student_record.html', student_data=student_data)


@app.route('/students/records/edit/<student_id>', methods=['GET', 'POST'])
@permission_required('editall')
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
            information_provider=form.information_provider.data,

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
            low_self_esteem=form.low_self_esteem.data,
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
            other=form.other_history.data,
            previous_treatments=form.previous_treatments.data,
            previous_treatments_likes_dislikes=form.previous_treatments_likes_dislikes.data,
            previous_treatments_learned=form.previous_treatments_learned.data,
            previous_treatments_like_to_continue=form.previous_treatments_like_to_continue.data,
            previous_hospital_stays_psych=form.previous_hospital_stays_psych.data,
            current_thoughts_to_harm=form.current_thoughts_to_harm.data,
            past_thoughts_to_harm=form.past_thoughts_to_harm.data,
            student_id=form.student_id.data
        )

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
            
            rel_qual_mother = form.rel_qual_mother.data,
            rel_qual_father = form.rel_qual_father.data,
            rel_qual_step_parent = form.rel_qual_step_parent.data,


            family_abuse_history=form.family_abuse_history.data,
            family_mental_history=form.family_mental_history.data,
            additional_information=form.additional_information_family.data,

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

        occupational_history = OccupationalHistory(
            employment_status=form.employment_status.data,
            satisfaction=form.satisfaction.data,
            satisfaction_reason=form.satisfaction_reason.data,
            student_id=form.student_id.data
        )

        substance_abuse_history = SubstanceAbuseHistory(
            struggled_with_substance_abuse=form.struggled_with_substance_abuse.data,

            alcohol=form.alcohol.data,
            alcohol_age_first_use=form.alcohol_age_first_use.data,
            alcohol_frequency_of_use=form.alcohol_frequency_of_use.data,
            alcohol_amount_used=form.alcohol_amount_used.data,
            alcohol_way_of_intake=form.alcohol_way_of_intake.data,

            cigarette=form.cigarette.data,
            cigarette_age_first_use=form.cigarette_age_first_use.data,
            cigarette_frequency_of_use=form.cigarette_frequency_of_use.data,
            cigarette_amount_used=form.cigarette_amount_used.data,
            cigarette_way_of_intake=form.cigarette_way_of_intake.data,
            
            marijuana=form.marijuana.data,
            marijuana_age_first_use=form.marijuana_age_first_use.data,
            marijuana_frequency_of_use=form.marijuana_frequency_of_use.data,
            marijuana_amount_used=form.marijuana_amount_used.data,
            marijuana_way_of_intake=form.marijuana_way_of_intake.data,

            cocaine=form.cocaine.data,
            cocaine_age_first_use=form.cocaine_age_first_use.data,
            cocaine_frequency_of_use=form.cocaine_frequency_of_use.data,
            cocaine_amount_used=form.cocaine_amount_used.data,
            cocaine_way_of_intake=form.cocaine_way_of_intake.data,

            heroin=form.heroin.data,
            heroin_age_first_use=form.heroin_age_first_use.data,
            heroin_frequency_of_use=form.heroin_frequency_of_use.data,
            heroin_amount_used=form.heroin_amount_used.data,
            heroin_way_of_intake=form.heroin_way_of_intake.data,

            amphetamines=form.amphetamines.data,
            amphetamines_age_first_use=form.amphetamines_age_first_use.data,
            amphetamines_frequency_of_use=form.amphetamines_frequency_of_use.data,
            amphetamines_amount_used=form.amphetamines_amount_used.data,
            amphetamines_way_of_intake=form.amphetamines_way_of_intake.data,

            club_drugs=form.club_drugs.data,
            club_drugs_age_first_use=form.club_drugs_age_first_use.data,
            club_drugs_frequency_of_use=form.club_drugs_frequency_of_use.data,
            club_drugs_amount_used=form.club_drugs_amount_used.data,
            club_drugs_way_of_intake=form.club_drugs_way_of_intake.data,

            pain_meds=form.pain_meds.data,
            pain_meds_age_first_use=form.pain_meds_age_first_use.data,
            pain_meds_frequency_of_use=form.pain_meds_frequency_of_use.data,
            pain_meds_amount_used=form.pain_meds_amount_used.data,
            pain_meds_way_of_intake=form.pain_meds_way_of_intake.data,

            benzo=form.benzo.data,
            benzo_age_first_use=form.benzo_age_first_use.data,
            benzo_frequency_of_use=form.benzo_frequency_of_use.data,
            benzo_amount_used=form.benzo_amount_used.data,
            benzo_way_of_intake=form.benzo_way_of_intake.data,


            other_meds=form.other_meds.data,
            other_meds_age_first_use=form.other_meds_age_first_use.data,
            other_meds_frequency_of_use=form.other_meds_frequency_of_use.data,
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
            to_work_on=form.to_work_on.data,
            expectations=form.expectations.data,
            things_to_change=form.things_to_change.data,
            other_information=form.other_information.data,
            
            student_id=form.student_id.data
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
            

            date_of_birth = form.date_of_birth.data,
            age = form.age.data,
            gender = form.gender.data,
            civil_status = request.form.get('civil'),
            nationality = form.nationality.data,
            religion = form.religion.data,
            residence = form.residence.data,
            contact_number = form.residence.data,
            email_address = form.email_address.data,

            history_information=history_info,
            health_information=health_info,
            family_background=family_background,
            social_history=social_history,
            educational_background=educational_background,
            occupational_history=occupational_history,
            substance_abuse_history=substance_abuse_history,
            legal_history=legal_history,
            additional_information=additional_info
        )

        # Add the new records to the database
        db.session.add(new_student)
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
