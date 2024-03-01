import pandas as pd
from flask import jsonify

from app import app, db
from app.models.models import *
from sqlalchemy.orm import joinedload

def process_data(student_id=None, search_query=None):
    with app.app_context():
        query = StudentInformation.query

        if student_id is not None:
            query = query.filter_by(student_id=student_id)

        if search_query:
            query = (
                query
                .join(PersonalInformation)
                .join(EducationalBackground)
                # .join(PsychologicalAssessments)
                .join(Course, Course.name == StudentInformation.course)
                .join(College, College.id == Course.college_id) 
                .filter(
                    (StudentInformation.student_id.ilike(f"%{search_query}%")) |
                    (StudentInformation.first_name.ilike(f"%{search_query}%")) |
                    (StudentInformation.last_name.ilike(f"%{search_query}%")) |
                    (StudentInformation.course.ilike(f"%{search_query}%")) |
                    (StudentInformation.year_level.ilike(f"%{search_query}%")) |
                    (StudentInformation.campus.ilike(f"%{search_query}%")) |
                    (PersonalInformation.sex.ilike(f"%{search_query}%")) |
                    (PersonalInformation.gender.ilike(f"%{search_query}%")) |
                    (PersonalInformation.religion.ilike(f"%{search_query}%")) |
                    (PersonalInformation.nationality.ilike(f"%{search_query}%")) |
                    (PersonalInformation.place_of_birth.ilike(f"%{search_query}%")) |
                    # (EducationalBackground.senior_high_school.ilike(f"%{search_query}%")) |
                    # (EducationalBackground.junior_high_school.ilike(f"%{search_query}%")) |
                    # (EducationalBackground.elementary_school.ilike(f"%{search_query}%")) |
                    # (PsychologicalAssessments.learning_styles.ilike(f"%{search_query}%")) |
                    # (PsychologicalAssessments.personality_test.ilike(f"%{search_query}%")) |
                    # (PsychologicalAssessments.iq_test.ilike(f"%{search_query}%")) |
                    (College.name.ilike(f"%{search_query}%"))
            )
        )

        data = (
            query
            .options(joinedload(StudentInformation.personal_information))
            .options(joinedload(StudentInformation.history_information))
            .options(joinedload(StudentInformation.health_information))
            .options(joinedload(StudentInformation.family_background))
            .options(joinedload(StudentInformation.social_history))
            .options(joinedload(StudentInformation.educational_background))
            .options(joinedload(StudentInformation.occupational_history))
            .options(joinedload(StudentInformation.substance_abuse_history))
            .options(joinedload(StudentInformation.legal_history))
            # .options(joinedload(StudentInformation.psychological_assessments))
            .options(joinedload(StudentInformation.additional_information))
            .options(joinedload(StudentInformation.visits))
            .all()
        )

        data_list = []
        for record in data:
            personal_information = record.personal_information
            history_information = record.history_information
            health_information = record.health_information
            family_background = record.family_background
            social_history = record.social_history
            educational_background = record.educational_background
            occupational_history = record.occupational_history
            substance_abuse_history = record.substance_abuse_history
            legal_history = record.legal_history
            additional_information = record.additional_information
            student_visits = record.visits

            course_name = record.course
            college = Course.query.filter_by(name=course_name).first()
            college_name = college.college.name if college else None 

            nature_of_concern = [visit.nature_of_concern for visit in record.visits]
            nature_of_concern_str = ', '.join(nature_of_concern)
            
            data_list.append({
                # Student Information
                'student_id': record.student_id,
                'last_name': record.last_name,
                'first_name': record.first_name,
                'course': course_name,
                'year_level': record.year_level,
                'campus': record.campus,
                'college': college_name,
                'year_level': record.year_level,

                # Personal Information
                'age': personal_information.age,
                'sex': personal_information.sex,
                'gender': personal_information.gender,
                'contact_number': personal_information.contact_number,
                'religion': personal_information.religion,
                'date_of_birth': personal_information.date_of_birth,
                'place_of_birth': personal_information.place_of_birth,
                'nationality': personal_information.nationality,
                'counseling_history': personal_information.counseling_history,
                'residence': personal_information.residence,

                # Family Background
                'father_age': family_background.father_age,
                'mother_age': family_background.mother_age,
                'father_last_name': family_background.father_last_name,
                'father_first_name': family_background.father_first_name,
                'mother_last_name': family_background.mother_last_name,
                'mother_first_name': family_background.mother_first_name,

                # # Psychological Assessments
                # 'learning_styles': psychological_assessments.learning_styles,
                # 'personality_test': psychological_assessments.personality_test,
                # 'iq_test': psychological_assessments.iq_test,
                'nature_of_concern': nature_of_concern_str,
            })
            
        df = pd.DataFrame(data_list)
        return df

def data_to_dict():
    data_df = process_data()
    data = data_df.to_dict(orient='records')

    return data

    
def data_analytics(first_metric, second_metric):
    df = process_data()
    data_mean = df.groupby(first_metric)[second_metric].mean().reset_index()
    data_dict = data_mean.to_dict(orient='records')

    return data_dict


def data_count(query):
    df = process_data()

    data_count = df[query].value_counts().reset_index()
    data_count.columns = [query, 'student_count']

    data_dict = data_count.to_dict(orient='records')
    return data_dict
