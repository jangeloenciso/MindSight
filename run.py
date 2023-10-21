from app import app
import MySQLdb

if __name__ == '__main__':

    try:
        conn = MySQLdb.connect(
            user=app.config["MYSQL_USER"], 
            passwd=app.config["MYSQL_PASSWORD"], 
            host=app.config["MYSQL_HOST"], 
            db=app.config["MYSQL_DB"]
        )
        print("Connected to MySQL successfully!")
    except MySQLdb.Error as e:
        print(f"Error: {e}")


    app.run(debug=True, host='localhost', port=5000)

