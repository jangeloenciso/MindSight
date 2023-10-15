from flask import Flask, render_template, request, url_for, session, redirect
from flask_mysqldb import MySQL
import re, hashlib

app = Flask(__name__)

app.secret_key = 'm1nd$16ht2023'

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "m1nd$16ht"
app.config["MYSQL_DB"] = "mindsight"


mysql = MySQL(app)

@app.route('/')
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
            cur.execute('''SELECT * FROM admins WHERE username = %s''', [_username])
            
            acc = cur.fetchone()

            if acc:
                prmpt = "Sorry, but the username is already taken"
            
            elif not re.match(r'[A-Za-z0-9]+', _username):
                prmpt = "Sorry, but username must contain only characters and numbers"
            
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', _email):
                prmpt = 'Sorry, Invalid email address'

            elif not _username or not _password or not _email:
                prmpt = 'Please fill out the form.'

            else:
                encrypt = _password + app.secret_key
                encrypt = hashlib.sha1(encrypt.encode())
                _password = encrypt.hexdigest()

                cur.execute('''INSERT INTO admins (fname, lname, username, email, password) VALUES (%s, %s, %s, %s, %s)''', [_fname, _lname, _username, _email, _password])
                mysql.connection.commit()
                prmpt = "You have successfully sign up!"
                
        else:
            prmpt = "Passwords are not the same"
        
    return render_template('signup.html', prmpt=prmpt)

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
        cur.execute('SELECT * FROM admins WHERE username = %s AND password = %s', [_username, _password])

        acc = cur.fetchone()

        if acc:
            session['loggedin'] = True
            session['id'] = acc[0]
            session['username'] = acc[3]
            return redirect(url_for('dashboard'))
        
        else:
            prmpt = 'Incorrect username/password!'
       
    return render_template('login.html', prmpt=prmpt)

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():

    if 'loggedin' in session:
        return render_template('dashboard.html', username = session['username'])
    
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)