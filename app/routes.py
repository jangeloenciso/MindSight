import os
from app import app
from flask import render_template, url_for, session, redirect, request
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import re, hashlib
import pandas as pd
import plotly.offline as plt
import plotly.express as px
from .data_processing import *
from .forms import *


mysql = MySQL(app)

@app.route('/')
@app.route('/login-form', methods=['POST', 'GET'])
def login():
    prmpt = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        _username = request.form['username']
        _password = request.form['password']

        encrypt = _password + app.secret_key
        encrypt = hashlib.sha1(encrypt.encode())
        _password = encrypt.hexdigest()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM developers WHERE username = %s AND password = %s', [_username, _password])

        acc = cur.fetchone()

        if acc:
            session['loggedin'] = True
            session['id'] = acc[0]
            session['username'] = acc[3]
            session['fname'] = acc[1]
            session['lname'] = acc[2]
            return redirect(url_for('dashboard'))
        
        else:
            prmpt = 'Your username/password is incorrect'
       
    return render_template('login.html', prmpt = prmpt)

@app.route('/signup-form', methods = ['POST', 'GET'])
def signup():
    prmpt = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:

        _fname = request.form['fname']
        _lname = request.form['lname']
        _username = request.form['username']
        _email = request.form['email']
        _password = request.form['password']
        _confirm = request.form['confirm']

        if _confirm == _password:

            cur = mysql.connection.cursor()
            cur.execute('''SELECT * FROM developers WHERE username = %s''', [_username])
            
            acc = cur.fetchone()

            if acc:
                msg1 = 'Sorry, but the username "'
                msg2 = (_username)
                msg3 = '" is already taken'
                prmpt = (msg1 + msg2 + msg3)
            
            elif not re.match(r'[A-Za-z0-9]+', _username):
                prmpt = "Sorry, but username must contain only characters and numbers"
            
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', _email):
                prmpt = 'Sorry, Invalid email address'
            
            elif len(_password) < 8:
                prmpt = "Make sure your password is at lest 8 letters"

            elif not _username or not _password or not _email:
                prmpt = 'Please fill out the form.'

            else:
                encrypt = _password + app.secret_key
                encrypt = hashlib.sha1(encrypt.encode())
                _password = encrypt.hexdigest()

                cur.execute('''INSERT INTO developers (fname, lname, username, email, password) VALUES (%s, %s, %s, %s, %s)''', [_fname, _lname, _username, _email, _password])
                mysql.connection.commit()
                prmpt = "You have successfully signed up!"
                
        else:
            prmpt = "Passwords are not the same"
        
    return render_template('signup.html', prmpt=prmpt)

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():

    if 'loggedin' in session:
    
        result_religion, result_college_summary, result_campus = generate_bar_graph(data, data_college_summary)
    
        return render_template('dashboard.html', fname = session['fname'], lname = session['lname'], result_college_summary=result_college_summary, result_campus=result_campus)

    return redirect(url_for('login'))

@app.route('/developers')
def developers():
   return render_template('developers.html', fname = session['fname'], lname = session['lname'])

@app.route('/admin')
def admin():
   return render_template('admin.html', fname = session['fname'], lname = session['lname'])

@app.route('/analytics', methods=['GET', 'POST'])
def analytics():

    form = UploadFileForm()

    result_religion, result_college_summary, result_campus = generate_bar_graph(data, data_college_summary)
    scatter_plot = generate_scatter_plot()
    pie_graph = generate_pie_graph()

    if form.validate_on_submit():
        file = form.file.data
        print(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER']))
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))

    return render_template('analytics.html', fname = session['fname'], lname = session['lname'], pie_graph = pie_graph, result_religion = result_religion, scatter_plot = scatter_plot, form=form)

@app.route('/students')
def students():
   return render_template('students.html', fname = session['fname'], lname = session['lname'])

@app.route('/settings')
def settings():
   return render_template('settings.html', fname = session['fname'], lname = session['lname'])
