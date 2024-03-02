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
            # hashed_password = bcrypt.generate_password_hash(_password).decode('utf-8')
            new_user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=_username, email=form.email.data, password=_password, role=_role)
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
        StudentInformation.query
        .options(
            joinedload(StudentInformation.personal_information),
            joinedload(StudentInformation.family_background),
            joinedload(StudentInformation.health_information),
            joinedload(StudentInformation.educational_background),
            joinedload(StudentInformation.social_history),
            joinedload(StudentInformation.history_information),
            joinedload(StudentInformation.occupational_history),
            joinedload(StudentInformation.substance_abuse_history),
            joinedload(StudentInformation.legal_history),
            joinedload(StudentInformation.additional_information)
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

    if form.validate_on_submit():  # If the form is submitted and validated
        # Create instances of related models and populate them with form data
        personal_info = PersonalInformation(
            age=form.age.data,
            sex=form.sex.data,
            gender=form.gender.data,
            contact_number=form.contact_number.data,
            religion=form.religion.data,
            date_of_birth=form.date_of_birth.data,
            place_of_birth=form.place_of_birth.data,
            nationality=form.nationality.data,
            counseling_history=form.counseling_history.data,
            residence=form.residence.data,
            civil_status=form.civil_status.data,
            student_id=form.student_id.data
        )
        
        history_info = HistoryInformation(
            information_provider=form.information_provider.data,
            current_problem=form.current_problem.data,
            problem_length=form.problem_length.data,
            stressors=form.stressors.data,
            substance_abuse=form.substance_abuse.data,
            addiction=form.addiction.data,
            # Populate other history information fields
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
            father_age=form.father_age.data,
            mother_age=form.mother_age.data,
            father_last_name=form.father_last_name.data,
            mother_last_name=form.mother_last_name.data,
            father_first_name=form.father_first_name.data,
            mother_first_name=form.mother_first_name.data,
            family_abuse_history=form.family_abuse_history.data,
            family_mental_history=form.family_mental_history.data,
            additional_information=form.additional_information.data,
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
            additional_information=form.additional_information_edu.data,
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
            # Populate other substance abuse history fields
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

        # Create an instance of the main StudentInformation model and associate related models
        new_student = StudentInformation(
            student_id=form.student_id.data,
            last_name=form.last_name.data,
            first_name=form.first_name.data,
            course=form.course.data,
            year_level=form.year_level.data,
            # gpa=form.gpa.data,
            campus=form.campus.data,
            personal_information=personal_info,
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

        # Redirect the user to a page displaying the newly added record
        return redirect(url_for('student_record', new_record_id=new_student.id))

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
