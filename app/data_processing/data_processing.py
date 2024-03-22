import pandas as pd
from flask import jsonify

from app import app, db
from app.models.models import *
from sqlalchemy.orm import joinedload
from sqlalchemy import func

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
            .options(joinedload(BasicInformation.referral_information))
            .options(joinedload(BasicInformation.case_note))
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
            referral_information = record.referral_information
            case_note = record.case_note
            sessions = record.sessions

            
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
                'submitted_on': record.submitted_on
            }

            history_information_data = {
                # History Information
                'information_provider': history_information.information_provider,
                'current_problem': history_information.current_problem,
                'problem_length': history_information.problem_length,
                'stressors': history_information.stressors,

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

                'previous_treatments' : history_information.previous_treatments,
                'previous_treatments_likes_dislikes': history_information.previous_treatments_likes_dislikes,
                'previous_treatments_learned': history_information.previous_treatments_learned,
                'previous_treatments_like_to_continue': history_information.previous_treatments_like_to_continue,

                'previous_hospital_stays_psych': history_information.previous_hospital_stays_psych,
                'current_thoughts_to_harm' : history_information.current_thoughts_to_harm,
                'past_thoughts_to_harm' : history_information.past_thoughts_to_harm
            }

            health_information_data = {  
                # Health Information   
                'medication_and_dose': health_information.medication_and_dose,

                'serious_ch_illnesses_history': health_information.serious_ch_illnesses_history,
                'head_injuries': health_information.head_injuries,
                'lose_consciousness': health_information.lose_consciousness,
                'convulsions_or_seizures': health_information.convulsions_or_seizures,
                'fever': health_information.fever,
                'allergies': health_information.allergies,

                'current_physical_health': health_information.current_physical_health,
                'last_check_up': health_information.last_check_up,
                'has_physician': health_information.has_physician,
                'physician_name': health_information.physician_name,
                'physician_email': health_information.physician_email,
                'physician_number': health_information.physician_number
            }

            family_background_data = {
                # Family Background
                'birth_location': family_background.birth_location,
                'raised_by': family_background.raised_by,
                'rel_qual_mother': family_background.rel_qual_mother,
                'rel_qual_father': family_background.rel_qual_father,
                'rel_qual_step_parent': family_background.rel_qual_step_parent,
                'rel_qual_other': family_background.rel_qual_other,

                'family_abuse_history': family_background.family_abuse_history,
                'family_mental_history': family_background.family_mental_history,
                'additional_information': family_background.additional_information,
                'siblings': family_background.siblings
            }

            social_history_data = {
                # Social History
                'relationship_with_peers': social_history.relationship_with_peers,
                'social_support_network': social_history.social_support_network,
                'hobbies_or_interests': social_history.hobbies_or_interests,
                'cultural_concerns': social_history.cultural_concerns
            }

            educational_background_data = {
                # Educational Background
                'educational_history': educational_background.educational_history,
                'highest_level_achieved': educational_background.highest_level_achieved,
                'additional_information_education': educational_background.additional_information
            }

            occupational_history_data = {
                # Occupational History
                'employment_status': occupational_history.employment_status,
                'satisfaction': occupational_history.satisfaction,
                'satisfaction_reason': occupational_history.satisfaction_reason
            }

            substance_abuse_history_data = {
                # Substance Abuse History
                'struggled_with_substance_abuse': substance_abuse_history.struggled_with_substance_abuse,
                'alcohol': substance_abuse_history.alcohol,
                'alcohol_age_first_use': substance_abuse_history.alcohol_age_first_use,
                'alcohol_frequency_of_use': substance_abuse_history.alcohol_frequency_of_use,
                'alcohol_amount_used': substance_abuse_history.alcohol_amount_used,
                'alcohol_way_of_intake': substance_abuse_history.alcohol_way_of_intake,

                'cigarette': substance_abuse_history.cigarette,
                'cigarette_age_first_use': substance_abuse_history.cigarette_age_first_use,
                'cigarette_frequency_of_use': substance_abuse_history.cigarette_frequency_of_use,
                'cigarette_amount_used': substance_abuse_history.cigarette_amount_used,
                'cigarette_way_of_intake': substance_abuse_history.cigarette_way_of_intake,

                'marijuana': substance_abuse_history.marijuana,
                'marijuana_age_first_use': substance_abuse_history.marijuana_age_first_use,
                'marijuana_frequency_of_use': substance_abuse_history.marijuana_frequency_of_use,
                'marijuana_amount_used': substance_abuse_history.marijuana_amount_used,
                'marijuana_way_of_intake': substance_abuse_history.marijuana_way_of_intake,

                'cocaine': substance_abuse_history.cocaine,
                'cocaine_age_first_use': substance_abuse_history.cocaine_age_first_use,
                'cocaine_frequency_of_use': substance_abuse_history.cocaine_frequency_of_use,
                'cocaine_amount_used': substance_abuse_history.cocaine_amount_used,
                'cocaine_way_of_intake': substance_abuse_history.cocaine_way_of_intake,

                'heroin': substance_abuse_history.heroin,
                'heroin_age_first_use': substance_abuse_history.heroin_age_first_use,
                'heroin_frequency_of_use': substance_abuse_history.heroin_frequency_of_use,
                'heroin_amount_used': substance_abuse_history.heroin_amount_used,
                'heroin_way_of_intake': substance_abuse_history.heroin_way_of_intake,

                'amphetamines': substance_abuse_history.amphetamines,
                'amphetamines_age_first_use': substance_abuse_history.amphetamines_age_first_use,
                'amphetamines_frequency_of_use': substance_abuse_history.amphetamines_frequency_of_use,
                'amphetamines_amount_used': substance_abuse_history.amphetamines_amount_used,
                'amphetamines_way_of_intake': substance_abuse_history.amphetamines_way_of_intake,

                'club_drugs': substance_abuse_history.club_drugs,
                'club_drugs_age_first_use': substance_abuse_history.club_drugs_age_first_use,
                'club_drugs_frequency_of_use': substance_abuse_history.club_drugs_frequency_of_use,
                'club_drugs_amount_used': substance_abuse_history.club_drugs_amount_used,
                'club_drugs_way_of_intake': substance_abuse_history.club_drugs_way_of_intake,

                'pain_meds': substance_abuse_history.pain_meds,
                'pain_meds_age_first_use': substance_abuse_history.pain_meds_age_first_use,
                'pain_meds_frequency_of_use': substance_abuse_history.pain_meds_frequency_of_use,
                'pain_meds_amount_used': substance_abuse_history.pain_meds_amount_used,
                'pain_meds_way_of_intake': substance_abuse_history.pain_meds_way_of_intake,

                'benzo': substance_abuse_history.benzo,
                'benzo_age_first_use': substance_abuse_history.benzo_age_first_use,
                'benzo_frequency_of_use': substance_abuse_history.benzo_frequency_of_use,
                'benzo_amount_used': substance_abuse_history.benzo_amount_used,
                'benzo_way_of_intake': substance_abuse_history.benzo_way_of_intake,

                'hallucinogens': substance_abuse_history.hallucinogens,
                'hallucinogens_age_first_use': substance_abuse_history.hallucinogens_age_first_use,
                'hallucinogens_frequency_of_use': substance_abuse_history.hallucinogens_frequency_of_use,
                'hallucinogens_amount_used': substance_abuse_history.hallucinogens_amount_used,
                'hallucinogens_way_of_intake': substance_abuse_history.hallucinogens_way_of_intake,

                'other_meds': substance_abuse_history.other_meds,
                'other_meds_age_first_use': substance_abuse_history.other_meds_age_first_use,
                'other_meds_frequency_of_use': substance_abuse_history.other_meds_frequency_of_use,
                'other_meds_amount_used': substance_abuse_history.other_meds_amount_used,
                'other_meds_way_of_intake': substance_abuse_history.other_meds_way_of_intake,

                'treatment_program_name': substance_abuse_history.treatment_program_name,
                'treatment_type': substance_abuse_history.treatment_type,
                'treatment_date': substance_abuse_history.treatment_date,
                'treatment_outcome': substance_abuse_history.treatment_outcome
            }

            legal_history_data = {
                # Legal History
                'pending_criminal_charges': legal_history.pending_criminal_charges,
                'on_probation': legal_history.on_probation,
                'has_been_arrested': legal_history.has_been_arrested,

                'convictions': legal_history.convictions
            }

            additional_information_data = {
                # Additional Information
                'nature_of_concern': additional_information.nature_of_concern,
                'counselor': additional_information.counselor,
                'personal_agreement': additional_information.personal_agreement,
                'personal_agreement_date': additional_information.personal_agreement_date,
                'status': additional_information.status,
                'remarks': additional_information.remarks,
                'referral_source': additional_information.referral_source,
                'emergency_name': additional_information.emergency_name,
                'emergency_relationship': additional_information.emergency_relationship,
                'emergency_address': additional_information.emergency_address,
                'emergency_contact': additional_information.emergency_contact,
                'to_work_on': additional_information.to_work_on,
                'expectations': additional_information.expectations,
                'things_to_change': additional_information.things_to_change,
                'other_information': additional_information.other_information,
            }

            referral_information_data = {}

            if referral_information:
                referral_information_data = {
                    'reason_for_referral': referral_information.reason_for_referral,
                    'receiving_agency': referral_information.receiving_agency,
                    'receiving_contact_number': referral_information.receiving_contact_number,
                    'receiving_name': referral_information.receiving_name,
                    'receiving_email': referral_information.receiving_email,
                    'office_address': referral_information.office_address,
                    'appointment_schedule': referral_information.appointment_schedule,

                    'client_signature': referral_information.client_signature,
                    'client_signature_date': referral_information.client_signature_date,
                    'counselor_signature': referral_information.counselor_signature,
                    'counselor_signature_date': referral_information.counselor_signature_date
    }

            # case_note_data = {
            #     'counselor_name': case_note.counselor_name,
            #     'interview_date': case_note.interview_date,
            #     'number_of_session': case_note.number_of_session,

            #     'subject_complaint': case_note.subject_complaint,
            #     'objective_assessment': case_note.objective_assessment,
            #     'plan_of_action': case_note.plan_of_action,
            #     'progress_made': case_note.progress_made
            # }

            # sessions_data = {
            #     'session_date': sessions.session_date,
            #     'session_time_start': sessions.session_time_start,
            #     'session_time_end': sessions.session_time_end,
            #     'session_follow_up': sessions.session_follow_up,
            #     'session_attended_by': sessions.session_attended_by
            # }

            merged_data = {
                **basic_information_data,
                **history_information_data,
                **health_information_data,
                **family_background_data,
                **social_history_data,
                **educational_background_data,
                **occupational_history_data,
                **substance_abuse_history_data,
                **legal_history_data,
                **additional_information_data,
                **referral_information_data,
                # # **case_note_data,
                # **sessions_data
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
    if df[second_metric].dtype in [int, float, bool]:
        data_mean = df.groupby(first_metric)[second_metric].mean().reset_index()
        data_dict = data_mean.to_dict(orient='records')
        print(data_dict)
    else:
        data_count = df[df[second_metric] == 'Yes'].groupby(first_metric)[second_metric].value_counts().unstack(fill_value=0).reset_index()
        data_dict = data_count.to_dict(orient='records')
        print(data_dict)

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




def get_total_cases(college=None, time_period=None, year=None, month=None):  # Add month parameter
    with app.app_context():
        query = db.session.query(func.count(BasicInformation.student_id))

        if college:
            query = query.filter(BasicInformation.college == college)

        if time_period and year:
            if time_period == 'yearly':
                query = query.filter(func.extract('year', BasicInformation.submitted_on) == year)
            elif time_period == 'quarterly':
                query = query.filter(func.extract('quarter', BasicInformation.submitted_on) == year)
            elif time_period == 'monthly':
                query = query.filter(func.extract('year', BasicInformation.submitted_on) == year)
                if month:  # Filter by specific month
                    query = query.filter(func.extract('month', BasicInformation.submitted_on) == month)
            elif time_period == 'semestral':
                # Assuming semesterly refers to two semesters in a year
                query = query.filter(func.extract('year', BasicInformation.submitted_on) == year)
                query = query.filter(func.extract('month', BasicInformation.submitted_on).between(1, 6))

        total_cases = query.scalar()
        return total_cases
