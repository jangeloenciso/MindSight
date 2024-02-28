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
# from flask_mail import Mail, Message
# import random

# mail = Mail(app)

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
        _role = form.role.data

        user = User.query.filter_by(username=_username).first()
        if user:
            prmpt = f'Sorry, but the username "{_username}" is already taken'
        else:
            hashed_password = bcrypt.generate_password_hash(_password).decode('utf-8')
            new_user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=_username, email=form.email.data, password=hashed_password, role=_role)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('dashboard'))
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
        flash('Your credentials have been updated successfully.', 'success')
        return redirect(url_for('dashboard'))


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

@app.route('/students')
@permission_required('viewall')
@login_required
def students():
    return render_template('students.html')

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
            'IHK': 'Institute of Human Kinetics'
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

    student = (
        StudentInformation.query
        .options(
            joinedload(StudentInformation.personal_information),
            joinedload(StudentInformation.family_background),
            joinedload(StudentInformation.health_information),
            joinedload(StudentInformation.educational_background),
            joinedload(StudentInformation.visits)
        )
    )

    form = StudentRecordForm(obj=student)

    if form.validate_on_submit():  # If the form is submitted and validated
        
        # last_name = form.last_name.data
        # first_name = form.first_name.data
        # course = form.course.data
        # student_id = form.student_id.data
        # age = form.age.data
        # sex = form.sex.data
        # gender = form.gender.data
        # contact_number = form.contact_number.data
        # religion = form.religion.data
        # date_of_birth = form.date_of_birth.data
        # place_of_birth = form.place_of_birth.data
        # nationality = form.nationality.data
        # counseling_history = form.counseling_history.data
        # residence = form.residence.data
        # father_age = form.father_age.data
        # mother_age = form.mother_age.data
        # father_last_name = form.father_last_name.data
        # mother_last_name = form.mother_last_name.data
        # father_first_name = form.father_first_name.data
        # mother_first_name = form.mother_first_name.data
        # height = form.height.data
        # weight = form.weight.data
        # sight = form.sight.data
        # hearing = form.hearing.data
        # speech = form.speech.data
        # general_health = form.general_health.data
        # experienced_sickness = form.experienced_sickness.data
        # senior_high_school = form.senior_high_school.data
        # shs_strand = form.shs_strand.data
        # shs_graduation_year = form.shs_graduation_year.data
        # junior_high_school = form.junior_high_school.data
        # jhs_graduation_year = form.jhs_graduation_year.data
        # elementary_school = form.elementary_school.data
        # elementary_graduation_year = form.elementary_graduation_year.data
        # learning_styles = form.learning_styles.data
        # personality_test = form.personality_test.data
        # iq_test = form.iq_test.data

        form.populate_obj(student)
        form.populate_obj(student.personal_information)
        form.populate_obj(student.family_background)
        form.populate_obj(student.health_information)
        form.populate_obj(student.educational_background)

        # new_record = student (
        #     last_name=last_name,
        #     first_name=first_name,
        #     course=course,
        #     student_id=student_id,
        #     age=age,
        #     sex=sex,
        #     gender=gender,
        #     contact_number=contact_number,
        #     religion=religion,
        # )

        # Add the new record to the database
        # db.session.add(new_record)
        # db.session.commit() 
        #     date_of_birth=date_of_birth,
        #     place_of_birth=place_of_birth,
        #     nationality=nationality,
        #     counseling_history=counseling_history,
        #     residence=residence,
        #     father_age=father_age,
        #     mother_age=mother_age,
        #     father_last_name=father_last_name,
        #     mother_last_name=mother_last_name,
        #     father_first_name=father_first_name,
        #     mother_first_name=mother_first_name,
        #     height=height,
        #     weight=weight,
        #     sight=sight,
        #     hearing=hearing,
        #     speech=speech,
        #     general_health=general_health,
        #     experienced_sickness=experienced_sickness,
        #     senior_high_school=senior_high_school,
        #     shs_strand=shs_strand,
        #     shs_graduation_year=shs_graduation_year,
        #     junior_high_school=junior_high_school,
        #     jhs_graduation_year=jhs_graduation_year,
        #     elementary_school=elementary_school,
        #     elementary_graduation_year=elementary_graduation_year,
        #     learning_styles=learning_styles,
        #     personality_test=personality_test,
        #     iq_test=iq_test
        # )

        # Add the new record to the database
        db.session.add(student)
        db.session.commit() 

        # Flash a success message
        flash('New student added successfully!', 'success')

        # Redirect the user to a page displaying the newly added record
        return redirect(url_for('student_record', new_record_id=student.id))

    # If the form is not submitted or not validated, or if it's a GET request, render the add record template
    return render_template('add_record-test.html', form=form)


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
