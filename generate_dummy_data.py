# Generates 200 dummy records for testing

import random
from datetime import date, timedelta
from faker import Faker
from app import db, app
from app.models import StudentInformation, PersonalInformation, FamilyBackground, HealthInformation, EducationalBackground, PsychologicalAssessments

course_names = [
    "Bachelor of Science in Mechanical Engineering",
    "Bachelor of Science in Architecture",
    "Bachelor of Science in Civil Engineering",
    "Bachelor of Science in Electrical Engineering",
    "Bachelor of Science in Electronics Engineering",
    "Bachelor of Science in Computer Engineering",
    "Bachelor of Science in Industrial Engineering (Boni Campus)",
    "Bachelor of Science in Information Technology (Boni Campus)",
    "Bachelor of Science in Instrumentation and Control Engineering (Boni Campus)",
    "Bachelor of Science in Mechatronics",
    "Bachelor of Science in Accountancy",
    "Bachelor of Science in Entrepreneurship",
    "Bachelor of Science in Office Administration",
    "Bachelor of Science in Business Administration major in Operations Management",
    "Bachelor of Science in Business Administration major in Marketing Management",
    "Bachelor of Science in Business Administration major in Financial Management",
    "Bachelor of Science in Business Administration major in Human Resource Management",
    "Bachelor of Secondary Education major in English",
    "Bachelor of Secondary Education major in Math",
    "Bachelor of Secondary Education major in Science (Boni Campus)",
    "Bachelor of Secondary Education major in Social Studies",
    "Bachelor of Secondary Education Major in Filipino",
    "Bachelor of Technical-Vocational Teacher Education major in Animation",
    "Bachelor of Technical-Vocational Teacher Education major in Computer Hardware Servicing",
    "Bachelor of Technical-Vocational Teacher Education major in Visual Graphic Design",
    "Bachelor or Technical-Vocational Teacher Education Major in Garments Fashion and Design",
    "Bachelor or Technical-Vocational Teacher Education Major in Electronics Technology",
    "Bachelor or Technical-Vocational Teacher Education Major in Welding and Fabrications Technology",
    "Bachelor of Science in Psychology",
    "Bachelor of Arts in Political Science",
    "Bachelor of Science in Statistics (Boni Campus)",
    "Bachelor of Science in Biology (Boni Campus)",
    "Bachelor of Science in Astronomy",
    "Institute of Human Kinetics",
    "Bachelor of Science in Physical Education (Boni Campus)"
]


with app.app_context():

    db.session.query(PersonalInformation).delete()
    db.session.query(FamilyBackground).delete()
    db.session.query(HealthInformation).delete()
    db.session.query(EducationalBackground).delete()
    db.session.query(PsychologicalAssessments).delete()
    db.session.query(StudentInformation).delete()
    db.session.commit()

    fake = Faker()

    def random_date(start_date, end_date):
        return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    
    def generate_student_id():
        year = random.randint(2020, 2023)
        student_number = str(random.randint(100000, 200000)).zfill(6)
        student_id = str(year) + "-" + str(student_number)
        print(f"Generated Student ID: {student_id}")
        return student_id

    for _ in range(200):
        student = StudentInformation(
            student_id=generate_student_id(),
            course = fake.random_element(elements=course_names),
            year_level=str(random.randint(1, 4)),
            gpa=random.uniform(1.0, 5.0)
        )

        db.session.add(student)

        personal_info = PersonalInformation(
            age=random.randint(18, 30),
            sex=fake.random_element(elements=("Male", "Female")),
            gender=fake.random_element(elements=("Male", "Female", "LGBTQ")),
            religion=fake.random_element(elements=("Catholic", "Islam", "Buddhism", "Muslim")),
            date_of_birth=random_date(date(1990, 1, 1), date(2005, 1, 1)),
            place_of_birth=fake.city(),
            nationality=fake.random_element(elements=("Filipino", "Non-Filipino")),
            counseling_history=fake.random_element(elements=("Yes", "No")),
            residence=fake.random_element(elements=("Family Home", "Guardian's Home", "School Dormitory", "Dormitory", "Others")),
            student=student
        )

        family_background = FamilyBackground(
            father_age=random.randint(35, 60),
            mother_age=random.randint(35, 60),
            student=student
        )

        health_info = HealthInformation(
            height=random.uniform(150, 190),
            weight=random.uniform(45, 120),
            sight=fake.random_element(elements=("With Glasses", "Without Glasses")),
            hearing=fake.random_element(elements=("Normal", "Impaired")),
            speech=fake.random_element(elements=("Normal", "Impaired")),
            general_health=fake.random_element(elements=("Excellent", "Good", "Fair", "Poor")),
            experienced_sickness=fake.random_element(elements=("Yes", "No")),
            student=student
        )

        edu_background = EducationalBackground(
            senior_high_school=fake.random_element(elements=("SHS A", "SHS B", "SHS C")),
            shs_strand=fake.random_element(elements=("STEM", "ABM", "HUMSS", "GAS", "Arts and Design", "TVL", "Sports")),
            shs_graduation_year=random.randint(2018, 2023),
            junior_high_school=fake.random_element(elements=("JHS X", "JHS Y", "JHS Z")),
            jhs_graduation_year=random.randint(2018, 2022),
            elementary_school=fake.random_element(elements=("ES 1", "ES 2", "ES 3")),
            elementary_graduation_year=random.randint(2015, 2017),
            student=student
        )

        psychological_assessments = PsychologicalAssessments(
            learning_styles=fake.random_element(elements=("Visual", "Auditory", "Kinesthetic")),
            personality_test=fake.random_element(elements=("Introvert", "Extrovert")),
            iq_test=fake.random_int(min=70, max=150),
            student=student
        )

        db.session.add(personal_info)
        db.session.add(family_background)
        db.session.add(health_info)
        db.session.add(edu_background)
        db.session.add(psychological_assessments)

        db.session.commit()

    db.session.close()
