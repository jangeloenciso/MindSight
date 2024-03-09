import pandas as pd
from flask import jsonify

from app import app, db
from app.models.models import *
from sqlalchemy.orm import joinedload

def process_data(student_id=None, search_query=None):
    with app.app_context():
        query = BasicInformation.query

        # print(query)

        if student_id is not None:
            query = query.filter_by(student_id=student_id)
            print("printing student")
            print(query)

        print(search_query)
            
        if search_query:
            query = (
                query
                .filter(
                    (BasicInformation.student_id.ilike(f"%{search_query}%")) |
                    (BasicInformation.first_name.ilike(f"%{search_query}%")) |
                    (BasicInformation.last_name.ilike(f"%{search_query}%")) |
                    (BasicInformation.course.ilike(f"%{search_query}%")) |
                    (BasicInformation.year_level.ilike(f"%{search_query}%")) |
                    (BasicInformation.campus.ilike(f"%{search_query}%")) |
                    (BasicInformation.gender.ilike(f"%{search_query}%")) |
                    (BasicInformation.religion.ilike(f"%{search_query}%")) |
                    (BasicInformation.nationality.ilike(f"%{search_query}%"))
            )
        )

        data = (
            query
            .options(joinedload(BasicInformation.history_information))
            .options(joinedload(BasicInformation.health_information))
            .options(joinedload(BasicInformation.family_background))
            .options(joinedload(BasicInformation.social_history))
            .options(joinedload(BasicInformation.educational_background))
            .options(joinedload(BasicInformation.occupational_history))
            .options(joinedload(BasicInformation.substance_abuse_history))
            .options(joinedload(BasicInformation.legal_history))
            .options(joinedload(BasicInformation.additional_information))
            .options(joinedload(BasicInformation.visits))
            .all()
        )

        data_list = []
        for record in data:
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


            nature_of_concern = [visit.nature_of_concern for visit in record.visits]
            nature_of_concern_str = ', '.join(nature_of_concern)
            
            data_list.append({
                # Student Information
                'student_id': record.student_id,
                'last_name': record.last_name,
                'first_name': record.first_name,
                'college': record.college,
                'course': record.course,
                'year_level': record.year_level,
                'campus': record.campus,
                'year_level': record.year_level,

                # Personal Information
                'age': record.age,
                'gender': record.gender,
                'contact_number': record.contact_number,
                'religion': record.religion,
                'date_of_birth': record.date_of_birth,
                'nationality': record.nationality,
                'residence': record.residence,

                # Family Background
                # TODO: ADD THE NEW SHIT

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
