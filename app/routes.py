import os
from app import app, db, bcrypt
from app.models.models import User
from flask import render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required
from .data_processing import *
from .forms import *
from flask_login import login_user
from app.forms.signup import SignupForm
from app.forms.login import LoginForm

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

@app.route('/developers')
@login_required
def developers():
   return render_template('developers.html')

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

@app.route('/students')
@login_required
def students():
   return render_template('students.html')


# Student components

@app.route('/students/cas')
@login_required
def cas():
   
   return render_template('students/cas.html')

@app.route('/students/cbea')
@login_required
def cbea():
   return render_template('students/cbea.html')

@app.route('/students/cea')
@login_required
def cea():
   return render_template('students/cea.html')

@app.route('/students/ced')
@login_required
def ced():
   return render_template('students/ced.html')

@app.route('/students/ihk')
@login_required
def ihk():
   return render_template('students/ihk.html')

@app.route('/settings')
@login_required
def settings():
   return render_template('settings.html')

@app.route('/students/departments')
@login_required
def departments():
   data = data_to_dict()

   return render_template('students/departments.html', data=data)

@app.route('/students/<student_id>')
def student_detail(student_id):
    data = process_data(student_id)
    student_data = data.to_dict(orient='records')
    print(student_data)

    return render_template('students/student_record.html', student_data=student_data)

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
