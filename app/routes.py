from app import app, db, bcrypt
from app.models.models import *
from sqlalchemy.orm import joinedload
from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required
from .data_processing import *
from .forms import *
from flask_login import login_user
from app.forms.signup import SignupForm
from app.forms.login import LoginForm
from app.forms.edit_record import EditStudentForm
from app.forms.add_record import AddStudentForm
import pytesseract
from PIL import Image

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

    return render_template('login.html', form=form)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignupForm()

    if form.validate_on_submit(): 

        _username = form.username.data
        _password = form.password.data

        user = User.query.filter_by(username=_username).first()
        if user:
            prmpt = f'Sorry, but the username "{_username}" is already taken'
        else:
            hashed_password = bcrypt.generate_password_hash(_password).decode('utf-8')
            new_user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=_username, email=form.email.data, password=hashed_password)
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

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/analytics', methods=['GET', 'POST'])
@login_required
def analytics():
    return render_template('analytics.html')

@app.route('/analytics/analysis')
@login_required
def metrics():
    return render_template('metrics.html')

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

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

@app.route('/students')
@login_required
def students():
    return render_template('students.html')

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
            'IHK': 'Institute of Human Kinetics'
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

    return render_template('students/student_record.html', student_data=student_data)


@app.route('/students/records/edit/<student_id>', methods=['GET', 'POST'])
@login_required
def edit_record(student_id):
    student = (
        StudentInformation.query
        .options(
            joinedload(StudentInformation.personal_information),
            joinedload(StudentInformation.family_background),
            joinedload(StudentInformation.health_information),
            joinedload(StudentInformation.educational_background),
            joinedload(StudentInformation.psychological_assessments),
            joinedload(StudentInformation.visits)
        )
        .filter_by(student_id=student_id)
        .first()
    )
    
    # if not student:
    #     flash('Student not found', 'danger')
    #     return redirect(url_for('college_records', college="CBEA"))

    form = EditStudentForm(obj=student)

    if form.validate_on_submit():
        form.populate_obj(student)
        form.populate_obj(student.personal_information)
        form.populate_obj(student.family_background)
        form.populate_obj(student.health_information)
        form.populate_obj(student.educational_background)
        form.populate_obj(student.psychological_assessments)

        db.session.commit()
        flash('Student record updated successfully', 'success')
        return redirect(url_for('student_record', student_id=student_id))
    
    print(form.errors)

    return render_template('students/edit_record.html', form=form, student_id=student_id, student=student)


@app.route('/students/records/add', methods=['GET', 'POST'])
@login_required
def add_record():
    form = AddStudentForm()  # Create an instance of the AddRecordForm

    if form.validate_on_submit():  # If the form is submitted and validated
        
        last_name = form.last_name.data
        first_name = form.first.name.data
        course = form.course.data
        student_id = form.student_id.data
        age = form.age.data
        sex = form.sex.data
        gender = form.gender.data
        contact_number = form.contact_number.data
        religion = form.religion.data

        new_record = Student(
            last_name=last_name,
            first_name=first_name,
            course=course,
            student_id=student_id,
            age=age,
            sex=sex,
            gender=gender,
            contact_number=contact_number,
            religion=religion,
        )

        # Add the new record to the database
        db.session.add(new_record)
        db.session.commit() 

        # Flash a success message
        flash('New student added successfully!', 'success')

        # Redirect the user to a page displaying the newly added record
        return redirect(url_for('student_record', new_record_id=new_record.id))

    # If the form is not submitted or not validated, or if it's a GET request, render the add record template
    return render_template('students/add_record.html', form=form)



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
