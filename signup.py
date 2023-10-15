from flask import Flask,render_template, request
from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'm1nd$16ht'
app.config['MYSQL_DB'] = 'mindsight'
 

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('signup.html')

@app.route('/signup-form', methods = ['POST', 'GET'])
def signup():
    prmpt = ''

    if request.method == 'POST':
        _fname = request.form['fname']
        _lname = request.form['lname']
        _username = request.form['username']
        _password = request.form['password']
        _confirm = request.form['confirm']

        if _confirm == _password:
            cur = mysql.connection.cursor()
            cur.execute('''INSERT INTO developers (fname, lname, username, password) VALUES (%s, %s, %s, %s)''', (_fname, _lname, _username, _password))
            mysql.connection.commit()
        else:
            prmpt = "Passwords are not the same"
    return render_template('login.html')    
if __name__ == '__main__':
    app.run(host='localhost', port=5000)