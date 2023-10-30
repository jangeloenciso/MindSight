import os
import pandas as pd
import plotly.express as px

from app import app, db
from app.models.models import *
from sqlalchemy.orm import joinedload

from flask import jsonify


with app.app_context():
    data = (
        StudentInformation.query
        .options(joinedload(StudentInformation.personal_information))
        .options(joinedload(StudentInformation.family_background))
        .options(joinedload(StudentInformation.health_information))
        .options(joinedload(StudentInformation.educational_background))
        .options(joinedload(StudentInformation.psychological_assessments))
        .all()
    )

def process_data(first_metric, second_metric):
    data_list = []
    for record in data:
        personal_information = record.personal_information
        college_information = record.college_information
        family_background = record.family_background
        health_information = record.health_information
        educational_background = record.educational_background
        psychological_assessments = record.psychological_assessments

        data_list.append({
            'student_id': record.student_id,
            'course': record.course,
            'campus': record.campus,
            'gpa': record.gpa,
            'year_level': record.year_level,
            'college': college_information.college,
            'age': personal_information.age,
            'gender': personal_information.gender,
            'religion': personal_information.religion,
            'nationality': personal_information.nationality,
        })

    df = pd.DataFrame(data_list)
    data_mean = df.groupby(first_metric)[second_metric].mean().reset_index()
    data_dict = data_mean.to_dict(orient='records')

    # print(data_dict)
    print(jsonify(data_dict))

    return data_dict
























data_directory = os.path.join(os.path.dirname(__file__), 'data')

# Analytics
dummy_data_past = os.path.join(data_directory, 'dummy_data.csv')
dummy_data_new= os.path.join(data_directory, 'new_data.csv')

# Dashboard
dummy_data_college_sum= os.path.join(data_directory, 'college_count.csv')

data_past = pd.read_csv(dummy_data_past)
data_new = pd.read_csv(dummy_data_new)
data_college_sum = pd.read_csv(dummy_data_college_sum)




def query_student_information():
    query = (
        db.session.query(
            StudentInformation,
            PersonalInformation,
            FamilyBackground,
            HealthInformation,
            EducationalBackground,
            PsychologicalAssessments,
            Course,
            College,
        )
        .join(PersonalInformation)
        .join(FamilyBackground)
        .join(HealthInformation)
        .join(EducationalBackground)
        .join(PsychologicalAssessments)
        .join(Course, StudentInformation.course == Course.name)
        .join(College, Course.college_id == College.id)
    )

    results = query.all()
    return results

# Call the function to get the joined data


# Loop through the results to access the data


# def print_result():
#     results = query_student_information()
#     for row in results:
#         # Each 'row' is a tuple containing data from different tables
#         student_info, personal_info, family_info, health_info, edu_info, psy_info, course, college = row

#         # Access attributes from each table
#         student_id = student_info.student_id
#         age = personal_info.age
#         father_age = family_info.father_age
#         # ... access other attributes from various tables

#         # Access college and course information
#         college_name = college.name
#         course_name = course.name

#         print(student_id, age, college_name, course_name)



def process_data_past(first_metric, second_metric):
    data = pd.read_csv(dummy_data_past)

    # calculates the mean
    average_scores = data.groupby(first_metric)[second_metric].mean().reset_index()
    data_average = average_scores.to_dict(orient='records')

    return data_average

def process_data_new(first, second):
    data = pd.read_csv(dummy_data_new)

    # calculates the mean
    # TODO: nag eerror sa mga percentage and non-numerical value
    average_scores = data.groupby(first)[second].mean().reset_index()
    data_average = average_scores.to_dict(orient='records')

    return data_average

def process_data_college_sum():
    data = pd.read_csv(dummy_data_college_sum)

    average_scores = data.groupby('Colleges')['Students'].mean().reset_index()
    data_average = average_scores.to_dict(orient='records')

    return data_average