from app import app
from flask import render_template, url_for, session, redirect, request
from flask_mysqldb import MySQL
import re, hashlib
import pandas as pd
import json
import plotly
import plotly.express as px
import config


# TODO: Create Config File
app.secret_key = app.config["SECRET_KEY"]

app.config["MYSQL_USER"]
app.config["MYSQL_HOST"]
app.config["MYSQL_DB"]
app.config["MYSQL_PASSWORD"]

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
        # # Reading the tips.csv file
        # data = pd.read_csv('identity.csv')


        # fig = px.pie(data, names='Gender', 
        #      height=300, width=600, 
        #      title='IDENTITY',
        #      color_discrete_sequence=['#DB9050', '#095371', '#6092C0'])
        
        # fig.savefig('/mindsight/identity.png')
        
        return render_template('dashboard.html', fname = session['fname'], lname = session['lname'])
    
    return redirect(url_for('login'))

@app.route('/developers')
def devs():
   return render_template('devs.html', fname = session['fname'], lname = session['lname'])

@app.route('/admin')
def admin():
   return render_template('admin.html', fname = session['fname'], lname = session['lname'])

@app.route('/analytics')
def analytics():
   return render_template('analytics.html', fname = session['fname'], lname = session['lname'])

@app.route('/student')
def stud():
   return render_template('stud.html', fname = session['fname'], lname = session['lname'])

@app.route('/settings')
def sett():
   return render_template('sett.html', fname = session['fname'], lname = session['lname'])

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)