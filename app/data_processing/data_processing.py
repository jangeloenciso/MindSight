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
            # print("printing student")
            # print(query)

        # print(search_query)
            
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
            .options(joinedload(BasicInformation.sessions))
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

            
            basic_information_data = {
                # Basic Information
                'student_id': record.student_id,
                'last_name': record.last_name,
                'first_name': record.first_name,
                'college': record.college,
                'course': record.course,
                'year_level': record.year_level,
                'campus': record.campus,
                'student_signature': record.student_signature,

                'age': record.age,
                'gender': record.gender,
                'contact_number': record.contact_number,
                'religion': record.religion,
                'date_of_birth': record.date_of_birth,
                'nationality': record.nationality,
                'residence': record.residence,
                'civil_status': record.civil_status,
                'email_address': record.email_address,
                'contact_number': record.contact_number,
                'phone_number': record.phone_number,
                'guardian_name': record.guardian_name,
                'guardian_address': record.guardian_address,
                'guardian_contact': record.guardian_contact,
                'submitted_on': record.submitted_on,
                
                # Additional Information
                'counselor': record.additional_information.counselor,
                'nature_of_concern': record.additional_information.nature_of_concern,
                'status': record.additional_information.status,
                'remarks': record.additional_information.remarks
            }

            history_information_data = {
                # History Information
                'substance_abuse': history_information.substance_abuse,
                'substance_abuse': history_information.substance_abuse,
                'addiction': history_information.addiction,
                'depression_sad_down_feelings': history_information.depression_sad_down_feelings,
                'high_low_energy_level': history_information.high_low_energy_level,
                'angry_irritable': history_information.angry_irritable,
                'loss_of_interest': history_information.loss_of_interest,
                'difficulty_enjoying_things': history_information.difficulty_enjoying_things,
                'crying_spells': history_information.crying_spells,
                'decreased_motivation': history_information.decreased_motivation,
                'withdrawing_from_people': history_information.withdrawing_from_people,
                'mood_swings': history_information.mood_swings,
                'black_and_white_thinking': history_information.black_and_white_thinking,
                'negative_thinking': history_information.negative_thinking,
                'change_in_weight_or_appetite': history_information.change_in_weight_or_appetite,
                'change_in_sleeping_pattern': history_information.change_in_sleeping_pattern,
                'suicidal_thoughts_or_plans': history_information.suicidal_thoughts_or_plans,
                'self_harm': history_information.self_harm,
                'homicidal_thoughts_or_plans': history_information.homicidal_thoughts_or_plans,
                'difficulty_focusing': history_information.difficulty_focusing,
                'feelings_of_hopelessness': history_information.feelings_of_hopelessness,
                'feelings_of_shame_or_guilt': history_information.feelings_of_shame_or_guilt,
                'feelings_of_inadequacy': history_information.feelings_of_inadequacy,
                'anxious_nervous_tense_feelings': history_information.anxious_nervous_tense_feelings,
                'panic_attacks': history_information.panic_attacks,
                'racing_or_scrambled_thoughts': history_information.racing_or_scrambled_thoughts,
                'bad_or_unwanted_thoughts': history_information.bad_or_unwanted_thoughts,
                'flashbacks_or_nightmares': history_information.flashbacks_or_nightmares,
                'muscle_tensions_aches': history_information.muscle_tensions_aches,
                'hearing_voices_or_seeing_things': history_information.hearing_voices_or_seeing_things,
                'thoughts_of_running_away': history_information.thoughts_of_running_away,
                'paranoid_thoughts': history_information.paranoid_thoughts,
                'feelings_of_frustration': history_information.feelings_of_frustration,
                'feelings_of_being_cheated': history_information.feelings_of_being_cheated,
                'perfectionism': history_information.perfectionism,
                'counting_washing_checking': history_information.counting_washing_checking,
                'distorted_body_image': history_information.distorted_body_image,
                'concerns_about_dieting': history_information.concerns_about_dieting,
                'loss_of_control_over_eating': history_information.loss_of_control_over_eating,
                'binge_eating_or_purging': history_information.binge_eating_or_purging,
                'rules_about_eating': history_information.rules_about_eating,
                'compensating_for_eating': history_information.compensating_for_eating,
                'excessive_exercise': history_information.excessive_exercise,
                'indecisiveness_about_career': history_information.indecisiveness_about_career,
                'job_problems': history_information.job_problems,
                'other': history_information.other,

                'previous_treatments' : history_information.previous_treatments
            }

            merged_data = {
                **basic_information_data,
                **history_information_data
            }

            data_list.append(merged_data)
            
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

# Works with ChartJS
def data_count(query, selected_year=None):
    df = process_data()

    # print(selected_year)

    if selected_year:
        df['year'] = pd.to_datetime(df['submitted_on']).dt.year
        df = df[df['year'] == int(selected_year)]
        print(df)

    data_count = df[query].value_counts().reset_index()
    data_count.columns = [query, 'student_count']

    data_dict = data_count.to_dict(orient='records')
    return data_dict

# Works with the progress bars
def data_count_dict(query, college=None):
    df = process_data()

    if college == 'College':
        college_departments = ['CBEA', 'CEA', 'CAS', 'IHK', 'CED']
        df = df[df['college'].isin(college_departments)]

    if college == 'SHS':
        df = df[df['college'] == 'SHS']

    if college == 'JHS':
        df = df[df['college'] == 'JHS']
    
    if college == 'GRAD':
        df = df[df['college'] == 'GRAD']

    if college == 'LLL':
        df = df[df['college'] == 'LLL']


    if query == 'nature_of_concern':
        categories = ['Academic', 'Career', 'Social', 'Personal']

        data_count = {category: 0 for category in categories}

        counts_from_df = df[query].value_counts()

        for category in categories:
            if category in counts_from_df:
                data_count[category] = int(counts_from_df[category])
        return data_count

    if query == 'religion':
        categories = [
            "Roman Catholic",
            "Islam",
            "Iglesia ni Cristo",
            "Seventh-day Adventist",
            "Aglipay",
            "Iglesia Filipina Independiente",
            "Bible Baptist Church",
            "United Church of Christ in the Philippines",
            "Jehova's Witness",
            "Church of Christ",
            "Mormonism",
            "Other",
            "Atheist",
            "Agnostic",
            "Prefer not to say"
        ]
        data_count = {category: 0 for category in categories}

        counts_from_df = df[query].value_counts()

        for category in categories:
            if category in counts_from_df:
                data_count[category] = int(counts_from_df[category])
        return data_count

    if query == 'gender':
        categories = ["Male", "Female", "LGBTQIA+"]
        data_count = {category: 0 for category in categories}

        counts_from_df = df[query].value_counts()

        for category in categories:
            if category in counts_from_df:
                data_count[category] = int(counts_from_df[category])
        return data_count
    
    if query == 'campus':
        categories = ["Boni", "Pasig"]
        data_count = {category: 0 for category in categories}

        counts_from_df = df[query].value_counts()

        for category in categories:
            if category in counts_from_df:
                data_count[category] = int(counts_from_df[category])
        return data_count

    data_count = df[query].value_counts().to_dict()
    return data_count



def data_history_information(college=None, selected_year=None):
    df = process_data()
    
    # add something for college i cant make it work fuck me

    if selected_year:
        df['year'] = pd.to_datetime(df['submitted_on']).dt.year
        df = df[df['year'] == int(selected_year)]

    if college == 'College':
        college_departments = ['CBEA', 'CEA', 'CAS', 'IHK', 'CED']
        df = df[df['college'].isin(college_departments)]

    if college == 'SHS':
        df = df[df['college'] == 'SHS']

    if college == 'JHS':
        df = df[df['college'] == 'JHS']
    
    if college == 'GRAD':
        df = df[df['college'] == 'GRAD']

    if college == 'LLL':
        df = df[df['college'] == 'LLL']

    # print(df)

    data_dict = {
        'Substance abuse/dependence': int(df['substance_abuse'].sum()),
        'Addiction': int(df['addiction'].sum()),
        'Depression/Sad/Down feelings': int(df['depression_sad_down_feelings'].sum()),
        'High/Low energy level': int(df['high_low_energy_level'].sum()),
        'Angry/Irritable': int(df['angry_irritable'].sum()),
        'Loss of interest in activities': int(df['loss_of_interest'].sum()),
        'Difficulty enjoying things': int(df['difficulty_enjoying_things'].sum()),
        'Crying spells': int(df['crying_spells'].sum()),
        'Decreased motivation': int(df['decreased_motivation'].sum()),
        'Withdrawing from people/Isolation': int(df['withdrawing_from_people'].sum()),
        'Mood Swings': int(df['mood_swings'].sum()),
        'Black and white thinking/All or nothing thinking': int(df['black_and_white_thinking'].sum()),
        'Negative thinking': int(df['negative_thinking'].sum()),
        'Change in weight or appetite': int(df['change_in_weight_or_appetite'].sum()),
        'Change in sleeping pattern': int(df['change_in_sleeping_pattern'].sum()),
        'Suicidal thoughts or plans/Thoughts of hurting yourself': int(df['suicidal_thoughts_or_plans'].sum()),
        'Self-harm/Cutting/Burning yourself': int(df['self_harm'].sum()),
        'Homicidal thoughts or plans/Thoughts of hurting others': int(df['homicidal_thoughts_or_plans'].sum()),
        'Poor concentration/Difficulty focusing': int(df['difficulty_focusing'].sum()),
        'Feelings of hopelessness/Worthlessness': int(df['feelings_of_hopelessness'].sum()),
        'Feelings of shame or guilt': int(df['feelings_of_shame_or_guilt'].sum()),
        'Feelings of inadequacy/Low self-esteem': int(df['feelings_of_inadequacy'].sum()),
        'Anxious/Nervous/Tense feelings': int(df['anxious_nervous_tense_feelings'].sum()),
        'Panic attacks': int(df['panic_attacks'].sum()),
        'Racing or scrambled thoughts': int(df['racing_or_scrambled_thoughts'].sum()),
        'Bad or unwanted thoughts': int(df['bad_or_unwanted_thoughts'].sum()),
        'Flashbacks/Nightmares': int(df['flashbacks_or_nightmares'].sum()),
        'Muscle tensions, aches, etc.': int(df['muscle_tensions_aches'].sum()),
        'Hearing voices/Seeing things not there': int(df['hearing_voices_or_seeing_things'].sum()),
        'Thoughts of running away': int(df['thoughts_of_running_away'].sum()),
        'Paranoid thoughts/Thoughts': int(df['paranoid_thoughts'].sum()),
        'Feelings of frustration': int(df['feelings_of_frustration'].sum()),
        'Feelings of being cheated': int(df['feelings_of_being_cheated'].sum()),
        'Perfectionism': int(df['perfectionism'].sum()),


        'Rituals of counting things, washing hands, checking locks, doors, stove, etc./Overly concerned about germs': int(df['counting_washing_checking'].sum()),
        'Distorted body image': int(df['distorted_body_image'].sum()),
        'Concerns about dieting': int(df['concerns_about_dieting'].sum()),
        'Feelings of loss of control over eating': int(df['loss_of_control_over_eating'].sum()),


        'Binge eating/Purging': int(df['binge_eating_or_purging'].sum()),
        'Rules about eating/Compensating for eating': int(df['rules_about_eating'].sum()),
        'Excessive exercise': int(df['excessive_exercise'].sum()),
        'Indecisiveness about career': int(df['indecisiveness_about_career'].sum()),
        'Job problems': int(df['job_problems'].sum())
    }


    return data_dict

