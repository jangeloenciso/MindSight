from flask import Flask,render_template, request
from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mindsight'
 
mysql = MySQL(app)
 
@app.route('/')
def form():
    cur = mysql.connection.cursor()
    cur.execute('''INSERT INTO developers (fname, lname, username, password) VALUES ('Marithe', 'dela Cruz', 'tet', 'tet_UI' )''')
    cur.execute('''INSERT INTO developers (fname, lname, username, password) VALUES ('Matthew', 'Bautista', 'matt', 'matt_UI' )''')
    cur.execute('''INSERT INTO developers (fname, lname, username, password) VALUES ('Justin Marley', 'Fontanilla', 'tin', 'tin_dev' )''')
    cur.execute('''INSERT INTO developers (fname, lname, username, password) VALUES ('Joseph Angelo', 'Enciso', 'joker', 'joker_dev' )''')
    cur.execute('''INSERT INTO developers (fname, lname, username, password) VALUES ('Jorge Robert', 'Velarde', 'jowjie', 'jowjie_dev' )''')
    return 'done'

if __name__ == '__main__':
    app.run(host='localhost', port=5000)