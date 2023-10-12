from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib

app = Flask(__name__)

mindisight = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="mindsight"
)

@app.route('/login-form', methods=['GET', 'POST'])
def login():
    return render_template('login.html', msg='')


@app.route('/login-form', methods = ['POST','GET'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username not in accounts:
        return render_template('login.html', info = 'Invalid User')
    else: 
        if accounts[username] != password:
            return render_template('login.html', info = 'Invalid Password')
        else:
            return render_template('welcome.html')
        
if __name__ == '__main__':
    app.run(debug=1, host='0.0.0.0', port=5001)
