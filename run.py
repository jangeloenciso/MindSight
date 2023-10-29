from app import app, db  # Import the app and the existing SQLAlchemy instance

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, host='localhost', port=5000)



