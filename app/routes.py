from app import app, db, bcrypt
from app.models.models import *
from sqlalchemy.orm import joinedload
from flask import render_template, url_for, redirect, flash, request, jsonify, send_file, session, current_app
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
from werkzeug.utils import secure_filename
import logging, os, smtplib, pyotp, time
from datetime import datetime
from sqlalchemy import desc, func, and_
import base64
from collections import defaultdict
from calendar import month_name
from email.mime.text import MIMEText


SECURITY_QUESTIONS = {
            'question1': 'In what city did your parents meet?',
            'question2': 'Where did you go on your first solo trip?',
            'question3': 'What was the first dish you learned to cook?',
            'question4': 'What was the name of your first stuffed toy?',
            'question5': 'What was the title of the first book you read?'
}

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app_dir = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(app_dir, 'uploads')

@app.before_request
def before_request():
    session.permanent = True

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
    
    if request.method == 'POST' and form.validate_on_submit():
        _email = form.email_address.data
        user = User.query.filter_by(email=_email).first()
            
        if user:
            secret = pyotp.random_base32()
            totp = pyotp.TOTP(secret)

            otp_value = totp.now()
            _username = user.username

            session['otp_secret_forgot'] = secret 
            session['otp_time_forgot'] = time.time()
            session['username'] = _username
    
            email = user.email
            send_otp_to_email_forgot(email, otp_value)
            print(otp_value)

            return jsonify({'success': True})
            
        else:
            print('User does not exist.', 'error')
            return jsonify({'error': True})
    
    return render_template('forgot.html', form=form)

# Send OTP to the registered email address
def send_otp_to_email_forgot(email, otp):
    sender = current_app.config['MAIL_USERNAME']
    recipients = [email]
    password = current_app.config['MAIL_PASSWORD']
    server = current_app.config['MAIL_SERVER']
    port = current_app.config['MAIL_PORT']

    msg = MIMEText(f'Your OTP Verification is: {otp}')
    msg['Subject'] = 'Mindsight OTP Verification'
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    with smtplib.SMTP(server, port) as smtp_server:
        smtp_server.ehlo() 
        smtp_server.starttls()
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())

# Render OTP form
@app.route('/otp_forgot-password', methods=['GET'])
def display_otp_form():

    return render_template('otp_forgot.html')

# Validate the OTP
@app.route('/otp_forgot-password', methods=['POST'])
def verify_otp_forgot():
    otp = request.json.get('otp')
    stored_otp = session.get('otp_secret_forgot')
    otp_time = session.get('otp_time_forgot')
    
    print('OTP', otp)
    session_timeout = current_app.config.get('SESSION_TIMEOUT')
    session_timeout_seconds = session_timeout.total_seconds()

    if stored_otp and otp_time and (time.time() - otp_time) <= session_timeout_seconds:
        totp = pyotp.TOTP(stored_otp)
        otp_number = totp.now()
        print('OTP Now', otp_number)
        if totp.verify(otp):
            print('success')
            return jsonify({'success': True})

    print('error: OTP verification failed')
    return jsonify({'error': True})


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPassword()

    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    print('Username:', user.username)
    
    if form.validate_on_submit():
        print('validated')

        if bcrypt.check_password_hash(user.security_answer, form.security_answer.data):
            new_password = form.password.data
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            user.password = hashed_password

            session.pop('otp_secret_forgot', None)
            session.pop('otp_time_forgot', None)

            # Commit changes to the database
            db.session.commit()
            return jsonify({'success': True})
    
        else:
            print('Incorrect security answer', 'error')
            return jsonify({'error': 'Incorrect security answer'})
        
    
    _security_question = user.security_question
    security_question = SECURITY_QUESTIONS.get(_security_question, 'Unknown Question')

    return render_template('reset.html', form=form, security_question=security_question)

# 404 Page
@app.route('/404')
def error():
    return render_template('error.html')


# Pages

@app.route('/dashboard')
@login_required
def dashboard():
    year = 2024
    history_data = data_history_information()
    concerns_data = data_count_dict('nature_of_concern')
    religion_data = data_count_dict('religion')
    campus_data = data_count_dict('campus')
    identity_data = data_count_dict('gender')

    college_names = [
        "CEA",
        "CBEA",
        "CED",
        "CAS",
        "IHK",
        "SHS",
        "JHS",
        "GRAD",
        "LLL"
    ]

    overall_monthly_total = defaultdict(int)  # Initialize overall monthly total

    month_names = {i: month_name[i] for i in range(1, 13)}

    for college in college_names:
        for month in range(1, 13):
            month_total = get_total_cases(college=college, time_period='monthly', year=year, month=month)
            overall_monthly_total[month_names[month]] += month_total  # Add the monthly total to the overall monthly total

    print("Overall Monthly Total:", dict(overall_monthly_total))

    # Fetching terminated cases data for each college
    terminated_data = {college: data_count_dict('status', college) for college in college_names}

    jhs_data = data_count_dict('status', 'JHS')
    shs_data = data_count_dict('status', 'SHS')
    college_data = data_count_dict('status', 'College')
    grad_data = data_count_dict('status', 'GRAD')
    lll_data = data_count_dict('status', 'LLL')

    return render_template('dashboard.html', terminated_data=terminated_data, religion_data=religion_data, identity_data=identity_data, campus_data=campus_data, history_data=history_data, concerns_data=concerns_data, overall_monthly_total=overall_monthly_total, jhs_data=jhs_data, shs_data=shs_data, college_data=college_data, grad_data=grad_data, lll_data=lll_data)


# pages for admin / viewing of students whose been counseled
@app.route('/admin')
@login_required
def admin():

    admin = User.query.all()

    for user in admin:
        user.full_name = user.first_name + ' ' + user.last_name

    # query all counseled students and organize it by latest to oldest (date)
    # Subquery to get the maximum interview_date for each student
        subquery = db.session.query(CaseNote.student_id, func.max(CaseNote.interview_date).label('max_interview_date')) \
                            .group_by(CaseNote.student_id).subquery()

        # query to get the last case note for each student
        students = db.session.query(CaseNote, BasicInformation, AdditionalInformation) \
                            .join(BasicInformation, CaseNote.student_id == BasicInformation.student_id) \
                            .join(AdditionalInformation, CaseNote.student_id == AdditionalInformation.student_id) \
                            .join(subquery, and_(subquery.c.student_id == CaseNote.student_id,
                                                subquery.c.max_interview_date == CaseNote.interview_date)).filter(BasicInformation.archived != True) \
                            .order_by(desc(CaseNote.interview_date)).all()

    # count the number of students counseled by each counselor
    students_count = db.session.query(AdditionalInformation.counselor, func.count(AdditionalInformation.id)) \
        .filter(and_(AdditionalInformation.counselor != None, AdditionalInformation.status != 'Terminated')) \
        .group_by(AdditionalInformation.counselor).all()

    # filter out terminated students
    active_students = {}
    for student in students:
        counselor = student[2].counselor
        if student[2].status != 'Terminated':
            if counselor not in active_students:
                active_students[counselor] = 1
            else:
                active_students[counselor] += 1

    students_count_dict = {counselor: count for counselor, count in students_count}

    print(students)

    return render_template('admin.html', admin=admin, students=students, students_count=students_count_dict, active_students=active_students)


@app.route('/admin/history')
@login_required
def counseling_history():
    full_name = request.args.get('full_name', default='', type=str)

    counselor_name = full_name

    # Subquery to get the maximum interview_date for each student
    subquery = db.session.query(CaseNote.student_id, func.max(CaseNote.interview_date).label('max_interview_date')) \
                         .group_by(CaseNote.student_id).subquery()

    # Query to get the last case note for each student
    students = db.session.query(CaseNote, BasicInformation, AdditionalInformation) \
                         .join(BasicInformation, CaseNote.student_id == BasicInformation.student_id) \
                         .join(AdditionalInformation, CaseNote.student_id == AdditionalInformation.student_id) \
                         .join(subquery, and_(subquery.c.student_id == CaseNote.student_id,
                                              subquery.c.max_interview_date == CaseNote.interview_date)) \
                         .filter(BasicInformation.archived != True) \
                         .order_by(desc(CaseNote.interview_date))

    # Filter by counselor_name if provided
    if counselor_name:
        students = students.filter(AdditionalInformation.counselor == counselor_name)

    students = students.all()

    active_cases_count = sum(1 for student in students if student[2].status != 'Terminated')

    return render_template('admin/counseling_history.html', full_name=full_name, students=students, active_cases_count=active_cases_count)




# analytics
@app.route('/analytics', methods=['GET', 'POST'])
@login_required
def analytics():
    return render_template('analytics.html')

@app.route('/analytics/analysis')
@login_required
def metrics():
    return render_template('metrics.html')


@app.route('/analytics/experiences')
@login_required
def experiences_expand():
    return render_template('experiences_expand.html')

@app.route('/analytics/religion')
@login_required
def religion_expand():
    return render_template('religion_expand.html')

# settings page
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():

    form = EditCredentials(request.form)
    
    if request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username 
        form.email.data = current_user.email
        

    if form.validate_on_submit():
        if not bcrypt.check_password_hash(current_user.password, form.current_password.data):
            return jsonify({'error': True})
        
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


@login_required
def send_otp_to_email_settings(email, otp):
    sender = current_app.config['MAIL_USERNAME']
    recipients = [email]
    password = current_app.config['MAIL_PASSWORD']
    server = current_app.config['MAIL_SERVER']
    port = current_app.config['MAIL_PORT']

    msg = MIMEText(f'Your OTP Verification is: {otp}')
    msg['Subject'] = 'Mindsight OTP Verification'
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    with smtplib.SMTP(server, port) as smtp_server:
        smtp_server.ehlo() 
        smtp_server.starttls()
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())


@app.route('/otp', methods=['POST'])
@login_required
def otp_settings():
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)

    otp_value = totp.now()

    session['otp_secret'] = secret 
    session['otp_time'] = time.time()


    email = current_user.email
    send_otp_to_email_settings(email, otp_value)
    print(otp_value)

    return jsonify({'success': True})


@app.route('/verify_otp', methods=['POST'])
@login_required
def verify_otp_settings():
    otp = request.json.get('otp') 
    
    stored_otp = session.get('otp_secret')
    otp_time = session.get('otp_time')
    
    print(otp)
    session_timeout = current_app.config.get('SESSION_TIMEOUT')
    session_timeout_seconds = session_timeout.total_seconds()

    if stored_otp and otp_time and (time.time() - otp_time) <= session_timeout_seconds:
        totp = pyotp.TOTP(stored_otp)
        print(totp)
        if totp.verify(otp):
            print('success')
            return jsonify({'success': True})
        
    session.pop('otp_secret', None)
    session.pop('otp_time', None)

    return jsonify({'error': True})


@app.route('/students/records/search/', methods=['GET'])
@login_required
def search():
    query = request.args.get('query')

    print(query)

    search_data = process_data(search_query=query)
    search_results = search_data.to_dict(orient='records')

    student_id = [record['student_id'] for record in search_results]

    records = BasicInformation.query.join(AdditionalInformation).filter(
        BasicInformation.student_id.in_(student_id), 
        BasicInformation.archived == False).all()

    return render_template('search.html', search_results=search_results, query=query, records=records)

# view archived records
@app.route('/students/records/archived/', methods=['GET'])
@login_required
def view_archived():
    data = data_to_dict()

    student_id = [record['student_id'] for record in data]

    records = BasicInformation.query.join(AdditionalInformation).filter(
        BasicInformation.student_id.in_(student_id), 
        BasicInformation.archived == True).all()

    return render_template('students/archive_record.html', records=records)


# retrieve all archived records(bulk)
@app.route('/students/records/bulk_retrieve', methods=['POST'])
@login_required
def bulk_retrieve_records():

    selected_records = request.json.get('records', [])
    print(selected_records)

    for student_id in selected_records:
        student = BasicInformation.query.filter_by(student_id=student_id).first()
        print(student)

        if student:

            student.archived = False
            db.session.commit()
        
        else: 
            return jsonify({'error': True})
        
    return jsonify({'success': True})


# retrieve record when record clicked(individual)
@app.route('/students/records/retrieve/<student_id>', methods=['POST'])
@login_required
def retrieve_record(student_id):

    student = BasicInformation.query.filter_by(student_id=student_id).first()

    if not student:
        return jsonify({'error': True})
    
    student.archived = False
    db.session.commit()

    return jsonify({'success': True})


@app.route('/students/records/view/<student_id>/print')
@login_required
def print_record(student_id):

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

    data = process_data(student_id)
    student_data = data.to_dict(orient='records')
    # print(student_data[0]['client_signature'])

    binary_student_signature = student_data[0]['student_signature']
    binary_student_signature_data = base64.b64encode(binary_student_signature).decode('utf-8')

    student_signature = f'<img src="data:image/jpeg;base64,{binary_student_signature_data}" alt="Client Signature">'

    client_signature = None
    counselor_signature = None
    
    if student.referral_information:
        binary_client_signature = student_data[0]['client_signature']
        binary_client_signature_data = base64.b64encode(binary_client_signature).decode('utf-8')

        client_signature = f'<img src="data:image/jpeg;base64,{binary_client_signature_data}" alt="Client Signature">'


        binary_counselor_signature = student.referral_information.counselor_signature
        binary_counselor_signature_data = base64.b64encode(binary_counselor_signature).decode('utf-8')

        counselor_signature = f'<img src="data:image/jpeg;base64,{binary_counselor_signature_data}" alt="Counselor Signature">'
    
    data = process_data(student_id)
    student_data = data.to_dict(orient='records')

    print(student_id)

    if len(student_data) == 0:
        # TODO: ADD A FLASH "STUDENT NOT FOUND"
        print("mayo amp")
        return redirect(url_for('students'))

    return render_template('print_record.html', student_data=student_data, student=student, client_signature=client_signature, counselor_signature=counselor_signature, student_signature=student_signature)

# Student components

@app.route('/level')
@login_required
def level():
    return render_template('level.html')


@app.route('/students/records/JHS/<int:year_level>')
@login_required
def jhs_records(year_level):
    data = data_to_dict()

    def college_name(year_level):
        college_dict = {
            7: 'Grade 7',
            8: 'Grade 8',
            9: 'Grade 9',
            10: 'Grade 10',
        }
        return college_dict.get(year_level)

    print(year_level)

    student_id = [student.student_id for student in BasicInformation.query.filter_by(year_level=year_level).all()]

    records = BasicInformation.query.join(AdditionalInformation).filter(
        BasicInformation.year_level == year_level, 
        BasicInformation.student_id.in_(student_id), 
        BasicInformation.archived == False).all()

    return render_template('students/records.html', year_level_name=college_name(year_level), year_level=year_level, data=data, records=records, student_id=student_id)


@app.route('/students/records/SHS/<course>')
@login_required
def shs_records(course):
    data = data_to_dict()

    def college_name(course):
        college_dict = {
            'STEM': 'Science, Technology, Engineering and Mathematics',
            'ABM': 'Accountancy, Business and Management',
            'HUMSS': 'Humanities and Social Sciences',
            'ICT': 'Information Communication and Technology',
        }
        return college_dict.get(course)
    
    print(college_name(course))

    student_id = [student.student_id for student in BasicInformation.query.filter_by(course=course).all()]

    records = BasicInformation.query.join(AdditionalInformation).filter(
        BasicInformation.course == course, 
        BasicInformation.student_id.in_(student_id), 
        BasicInformation.archived == False).all()

    return render_template('students/records.html', course_name=college_name(course), course=course, data=data, records=records, student_id=student_id)


@app.route('/students/records/COLLEGE/<college>')
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

    student_id = [student.student_id for student in BasicInformation.query.filter_by(college=college).all()]

    records = BasicInformation.query.join(AdditionalInformation).filter(
        BasicInformation.college == college, 
        BasicInformation.student_id.in_(student_id), 
        BasicInformation.archived == False).all()

    return render_template('students/records.html', college_name=college_name(college), college=college, data=data, records=records, student_id=student_id)

@app.route('/graduate')
@login_required
def graduate():
    return render_template('graduate.html')

@app.route('/students/records/GRADUATE/<college>')
@login_required
def graduate_records(college):
    data = data_to_dict()

    def college_name(college):
        college_dict = {
            'GRAD': 'Graduate',
        }
        return college_dict.get(college)

    print(college_name(college))

    student_id = [student.student_id for student in BasicInformation.query.filter_by(college=college).all()]

    records = BasicInformation.query.join(AdditionalInformation).filter(
        BasicInformation.college == college, 
        BasicInformation.student_id.in_(student_id), 
        BasicInformation.archived == False).all()

    return render_template('students/records.html', college_name=college_name(college), college=college, data=data, records=records, student_id=student_id)

@app.route('/LLL')
@login_required
def lll():
    return render_template('lll.html')

@app.route('/students/records/LLL/<college>')
@login_required
def lll_records(college):
    data = data_to_dict()

    def college_name(college):
        college_dict = {
            'LLL': 'Lifelong Learners',
        }
        return college_dict.get(college)

    print(college_name(college))

    student_id = [student.student_id for student in BasicInformation.query.filter_by(college=college).all()]

    records = BasicInformation.query.join(AdditionalInformation).filter(
        BasicInformation.college == college, 
        BasicInformation.student_id.in_(student_id), 
        BasicInformation.archived == False).all()

    return render_template('students/records.html', college_name=college_name(college), college=college, data=data, records=records, student_id=student_id)

# bulk archive student record
@app.route('/students/records/bulk_archive', methods=['POST'])
@login_required
def bulk_archive_records():

    selected_records = request.json.get('records', [])
    print(selected_records)

    for student_id in selected_records:
        student = BasicInformation.query.filter_by(student_id=student_id).first()
        print(student)

        if student:

            student.archived = True
            db.session.commit()
        
        else: 
            return jsonify({'error': True})
        
    return jsonify({'success': True})


# archive student record(individual)
@app.route('/students/records/view/archive/<student_id>', methods=['POST'])
@login_required
def archive_record(student_id):

    student = BasicInformation.query.filter_by(student_id=student_id).first()

    if not student:
        return jsonify({'error': True})
    
    student.archived = True
    db.session.commit()

    return jsonify({'success': True})


@app.route('/students/records/view/<student_id>')
@login_required
def student_record(student_id):
    data = process_data(student_id)
    student_data = data.to_dict(orient='records')

    student_signature_binary_data = student_data[0]['student_signature']
    student_signature_base64 = base64.b64encode(student_signature_binary_data).decode('utf-8')
    print(student_id)

    return render_template('students/student_record.html', student_id=student_id, student_data=student_data, student_signature = student_signature_base64)


@app.route('/students/records/view/full_record/<student_id>', methods=['GET', 'POST'])
@login_required
def full_record(student_id):


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

    data = process_data(student_id)
    student_data = data.to_dict(orient='records')
    # print(student_data[0]['client_signature'])

    binary_student_signature = student_data[0]['student_signature']
    binary_student_signature_data = base64.b64encode(binary_student_signature).decode('utf-8')

    student_signature = f'<img src="data:image/jpeg;base64,{binary_student_signature_data}" alt="Client Signature">'

    client_signature = None
    counselor_signature = None
    
    if student.referral_information:
        binary_client_signature = student_data[0]['client_signature']
        binary_client_signature_data = base64.b64encode(binary_client_signature).decode('utf-8')

        client_signature = f'<img src="data:image/jpeg;base64,{binary_client_signature_data}" alt="Client Signature">'


        binary_counselor_signature = student.referral_information.counselor_signature
        binary_counselor_signature_data = base64.b64encode(binary_counselor_signature).decode('utf-8')

        counselor_signature = f'<img src="data:image/jpeg;base64,{binary_counselor_signature_data}" alt="Counselor Signature">'

    print(student.referral_information)
    
    return render_template('students/full_record.html', student_id=student_id, student_data=student_data, student=student, client_signature=client_signature, counselor_signature=counselor_signature, student_signature=student_signature)

# extensions for accepted documents
def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# upload template
@app.route('/students/records/upload_record/<student_id>', methods=['GET', 'POST'])
def upload_record(student_id):

    data = process_data(student_id)
    student_data = data.to_dict(orient='records')

    documents = Document.query.filter_by(student_id=student_id, archived=False).all()

    return render_template('students/upload_record.html', student_id=student_id, student_data=student_data, documents=documents)

# upload of documents
@app.route('/students/records/upload_record/upload_file/<student_id>', methods=['POST'])
def upload_file(student_id):

    print(student_id)
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    print(UPLOAD_FOLDER)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # saves file
        file.save(file_path)

        # add new document and store in database
        new_document = Document(filename=filename, path=file_path, student_id=student_id)
        db.session.add(new_document)
        db.session.commit()

        return jsonify({'message': 'File uploaded successfully'}), 200
    else:
        return jsonify({'error': 'File upload failed'}), 500

# viewing of uploaded file
@app.route('/students/records/upload_record/view_document/<student_id>/<filename>')
def view_file(student_id, filename):

    document = Document.query.filter_by(student_id=student_id, filename=filename).first()
    
    if document:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        print(file_path)

        if os.path.exists(file_path):
            return send_file(file_path, mimetype='image/png/jpg/jpeg')
        
        else:
            return "File not found", 404
    else:
        return "File not found", 404

# archiving of uploaded file
@app.route('/students/records/upload_record/delete_file/<filename>', methods=['POST'])
def delete_file(filename):

    file = Document.query.filter_by(filename=filename).first()

    if file:
        file.archived = True
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'error': True})


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

            referral = ReferralInformation(
                reason_for_referral = form.reason_for_referral.data,
                receiving_agency = form.receiving_agency.data,
                receiving_contact_number = form.receiving_contact_number.data,
                receiving_name = form.receiving_name.data,
                receiving_email = form.receiving_email.data,
                office_address = form.office_address.data,
                appointment_schedule = form.appointment_schedule.data,

                client_signature = base64.b64decode(request.form['clientSignatureInput']),

                counselor_signature = base64.b64decode(request.form['counselorSignatureInput']),
                

                student_id = student_id
            )

            client_signature_date = request.form.get('refinfoclientdate')
            counselor_signature_date = request.form.get('refinfocounselordate')

            if client_signature_date:
                student.referral_information.client_signature_date = client_signature_date
                student.referral_information.counselor_signature_date = counselor_signature_date

            db.session.add(referral)
            
            status = request.form.get('status')
            student.additional_information.status = status

            remarks = request.form.get('remarks')
            student.additional_information.remarks = remarks

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
            if len(sibling_names) < len(existing_siblings):
        # Delete sibling records that were removed from the form
                for sibling in existing_siblings[len(sibling_names):]:
                    db.session.delete(sibling)

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
                    if conviction_dates[conviction_index]:
                        if len(convictions) >= 1:
                            new_conviction = Conviction(
                                conviction=conviction,
                                conviction_date=conviction_dates[conviction_index],
                                conviction_outcome=conviction_outcomes[conviction_index],
                                legal_history=student.legal_history
                            )
                            db.session.add(new_conviction)
            if len(convictions) < len(existing_convictions):
                for conviction in existing_convictions[len(convictions):]:
                    db.session.delete(conviction)   
        
            counselor_list = request.form.getlist('counselorName')
            interview_date = request.form.getlist('interviewDate')
            number_of_session = request.form.getlist('numberOfSession')
            subject_complaint = request.form.getlist('subjectComplaint')
            objective_assessment = request.form.getlist('objectiveAssessment')
            plan_of_action = request.form.getlist('planOfAction')
            progress_made = request.form.getlist('progressMade')

            if any(counselor_list) or any(interview_date) or any(number_of_session) or any(subject_complaint) or any(objective_assessment) or any(plan_of_action) or any(progress_made):
                for case_note_index, counselor_name in enumerate(counselor_list):
                    existing_case_note = CaseNote.query.filter_by(
                    counselor_name=counselor_name,
                    interview_date=interview_date[case_note_index],
                    number_of_session=number_of_session[case_note_index],
                    subject_complaint=subject_complaint[case_note_index],
                    objective_assessment=objective_assessment[case_note_index],
                    plan_of_action=plan_of_action[case_note_index],
                    progress_made=progress_made[case_note_index],
                    student_id=student.student_id
                ).first()
                if not existing_case_note:
                    new_case_note = CaseNote(
                        counselor_name=counselor_name,
                        interview_date=interview_date[case_note_index],
                        number_of_session=number_of_session[case_note_index],
                        subject_complaint=subject_complaint[case_note_index],
                        objective_assessment=objective_assessment[case_note_index],
                        plan_of_action=plan_of_action[case_note_index],
                        progress_made=progress_made[case_note_index],
                        student_id=student.student_id
                    )
                    db.session.add(new_case_note)

            existing_sessions = student.sessions

            session_date = request.form.getlist('sessionDate')
            session_time_start = request.form.getlist('sessionTimeStart')
            session_time_end = request.form.getlist('sessionTimeEnd')
            session_follow_up = request.form.getlist('sessionFollowUp')
            session_attended_by = request.form.getlist('sessionAttendedBy')

            for session_index, date in enumerate(session_date):
                if date:
                    if session_index < len(existing_sessions):
                        existing_session = existing_sessions[session_index]
                        existing_session.session_date = date
                        existing_session.session_time_start = session_time_start[session_index]
                        existing_session.session_time_end = session_time_end[session_index]
                        existing_session.session_follow_up = session_follow_up[session_index]
                        existing_session.session_attended_by = session_attended_by[session_index]
                    else:
                        new_session = Sessions(
                            session_date=date,
                            session_time_start=session_time_start[session_index],
                            session_time_end=session_time_end[session_index],
                            session_follow_up=session_follow_up[session_index],
                            session_attended_by=session_attended_by[session_index],
                            student_id=student.student_id
                        )
                        db.session.add(new_session)

            db.session.commit()



            db.session.commit()
            print('Student record updated successfully', 'success')
            return jsonify({'success': True, 'student_id': student_id})
            # return redirect(url_for('student_record', student_id=student_id))
        else:
            errors = form.errors
            print(form.errors)

    return render_template('students/edit_record.html', form=form, student_id=student_id, student=student)


@app.route('/student_id_form', methods=['POST', 'GET'])
def student_id_form():

    if request.method == 'POST':
        student_id = request.form.get('student_id')
        print(student_id)
        if student_id:
            return redirect(url_for('add_record', student_id=student_id))
        else:
            return render_template('student_id.html', student_id=student_id)
        
    return render_template('student_id.html')

# TODO: prepopulate other fields if and only if student already exist
@app.route('/add', methods=['GET', 'POST'])
def add_record():
    student_id = request.args.get('student_id')
    form = StudentRecordForm()

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

    if student_id:
        existing_student = BasicInformation.query.filter_by(student_id=student_id).first()
        if existing_student:
            form = StudentRecordForm(obj=existing_student)
        else:
            form.student_id.data = student_id

    if form.validate_on_submit():
        form.populate_obj(student.family_background)
        form.populate_obj(student.health_information)
        form.populate_obj(student.educational_background)
        form.populate_obj(student.social_history)
        form.populate_obj(student.history_information)
        form.populate_obj(student.occupational_history)
        form.populate_obj(student.substance_abuse_history)
        form.populate_obj(student.legal_history)
        form.populate_obj(student.additional_information)


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
            personal_agreement=form.personal_agreement.data,
            personal_agreement_date=request.form.get('personal_agreement_date'),
            # personal_agreement_date = form.personal_agreement_date.data,

            nature_of_concern=request.form.get('nature_of_concern'),
            counselor=form.counselor.data,

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

        date_of_birth = request.form.get('date_of_birth')

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

            age = form.age.data,
            gender = request.form.get('gender'),
            civil_status = request.form.get('civil'),
            nationality = form.nationality.data,
            religion = request.form.get('religion'),
            residence = form.residence.data,
            contact_number = form.contact_number.data,
            phone_number = form.phone_number.data,
            email_address = form.email_address.data,

            student_signature = base64.b64decode(request.form['signatureCanvasInput']),

            submitted_on = datetime.now(),

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

        if date_of_birth:
            new_student.date_of_birth = date_of_birth

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
        errors = form.errors
        print(request.form.get('signatureCanvasInput'))
        logging.error("Form validation failed")
        logging.error('ERRORS:', form.errors)

    current_date_and_time = datetime.now().strftime('%Y-%m-%dT%H:%M')

    return render_template('add_record.html', form=form, errors=errors, student_id=student_id, current_date_and_time=current_date_and_time)

@app.route('/print_report/<selected_year>')
def print_report(selected_year):
    year = selected_year

    college_names = [
        "CEA",
        "CBEA",
        "CED",
        "CAS",
        "IHK",
        "SHS",
        "JHS",
        "GRAD",
        "LLL"
    ]

    total_cases_dict = {}
    overall_total = defaultdict(int)
    overall_monthly_total = defaultdict(int)  # Initialize overall monthly total

    for college in college_names:
        college_total = {}
        for time_period in ['yearly', 'monthly']:  # Remove 'quarterly' from the time periods
            if time_period == 'monthly':
                college_total[time_period] = {}  # Initialize a nested dictionary for monthly totals
                for month in range(1, 13):
                    month_total = get_total_cases(college=college, time_period=time_period, year=year, month=month)
                    college_total[time_period][month] = month_total
                    overall_total[time_period] += month_total
                    overall_monthly_total[month] += month_total  # Add the monthly total to the overall monthly total
            else:
                college_total[time_period] = get_total_cases(college=college, time_period=time_period, year=year)
                overall_total[time_period] += college_total[time_period]
        total_cases_dict[college] = college_total

    print("Overall Total:", dict(overall_total))
    print("College-wise Total:", total_cases_dict)
    print("Overall Monthly Total:", dict(overall_monthly_total))  # Print the overall monthly total

    return render_template('generate_report.html', year=year, overall_total=dict(overall_total), college_totals=total_cases_dict, overall_monthly_total=dict(overall_monthly_total))




# API endpoints
@app.route('/get_cases/<selected_year>', methods=['GET'])
def get_cases(selected_year=None):
    year = selected_year
    if selected_year is None:
        year = datetime.now().year

    # Define the college groups to combine counts
    college_groups = {
        'College': ["CEA", "CBEA", "IHK", "CAS", "CED"],
        'SHS': ["SHS"],
        'JHS': ["JHS"],
        'GRAD': ["GRAD"],
        'LLL': ["LLL"]
    }

    total_cases_dict = {}
    overall_total = defaultdict(int)
    overall_monthly_total = defaultdict(int)

    for group_name, colleges in college_groups.items():
        group_total = {}
        for time_period in ['yearly', 'monthly']:
            if time_period == 'monthly':
                group_total[time_period] = {}
                for month in range(1, 13):
                    month_total = sum(get_total_cases(college=college, time_period=time_period, year=year, month=month) for college in colleges)
                    group_total[time_period][month] = month_total
                    overall_total[time_period] += month_total
                    overall_monthly_total[month] += month_total 
            else:
                group_total[time_period] = sum(get_total_cases(college=college, time_period=time_period, year=year) for college in colleges)
                overall_total[time_period] += group_total[time_period]
        total_cases_dict[group_name] = group_total

    print("Overall Total:", dict(overall_total))
    print("Group-wise Total:", total_cases_dict)
    print("Overall Monthly Total:", dict(overall_monthly_total))
    combined_data = {
        'total_cases_dict': total_cases_dict,
        'overall_total': dict(overall_total)
    }
    return jsonify(combined_data)


@app.route('/get_data/<first_metric>/<second_metric>', methods=['GET'])
def get_data(first_metric, second_metric):
    data = data_analytics(first_metric, second_metric)
    return jsonify(data)

@app.route('/get_data/<data_to_count>', methods=['GET'])
def get_data_count(data_to_count):
    data = data_count(data_to_count)
    return jsonify(data)

@app.route('/get_data/compare/<data_to_count>/<selected_year1>/<selected_year2>', methods=['GET'])
def get_data_year(data_to_count, selected_year1, selected_year2):

    if data_to_count == 'experiences':
        data1 = data_history_information(selected_year=selected_year1)
        data2 = data_history_information(selected_year=selected_year2)
    else:
        data1 = data_count(data_to_count, selected_year1)
        data2 = data_count(data_to_count, selected_year2)
    return jsonify({'data1': data1, 'data2': data2})
