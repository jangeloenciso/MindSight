import mysql.connector


mindisight = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="mindsight"
)


cursor = mindisight.cursor()

sql = "INSERT INTO developers (id, fname, lname, username, password) VALUES (%s, %s, %s, %s, %s)"
val = [
  ('', 'Marithe', 'dela Cruz', 'tet', 'tet_UI'),
  ('', 'Justin Marley', 'Fontanilla', 'tin', 'tin_dev'),
  ('', 'Matthew', 'Bautista', 'matt', 'matt_UI'),
  ('', 'Joseph Angelo', 'Enciso', 'joker', 'joker_dev'),
  ('', 'Jorge Robert', 'Velarde', 'jowjie', 'jowjie_dev')
]

cursor.executemany(sql, val)

mindisight.commit()

print(cursor.rowcount, "data was inserted.")