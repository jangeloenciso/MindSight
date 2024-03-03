from app import app, db
from app.models.models import *
import pytest
from flask_wtf import csrf
from flask_wtf.csrf import CSRFProtect
    
def test_add_record():

    form_data = {
    'student_id': '2020-887434',
    'last_name': 'Smith',
    'first_name': 'Emily',
    'course': 'Psychology',
    'year_level': 'Junior',
    'campus': 'Main Campus',
    'date_of_birth': '1999-05-15',
    'age': 25,
    'gender': 'Female',
    'civil_status': 'Single',
    'nationality': 'Canadian',
    'religion': 'None',
    'residence': '789 Elm St, City',
    'email_address': 'emily.smith@example.com',
    'contact_number': '123-456-7890',
    'guardian_name': 'David Smith',
    'guardian_address': '789 Elm St, City',
    'guardian_contact': '987-654-3210',
    'information_provider': 'School counselor',
    'current_problem': 'Stress and anxiety',
    'problem_length': '1 year',
    'stressors': 'Work and personal life balance',
    'substance_abuse': True,
    'addiction': False,
    'depression_sad_down_feelings': True,
    'high_low_energy_level': False,
    'angry_irritable': True,
    'loss_of_interest': False,
    'difficulty_enjoying_things': True,
    'crying_spells': False,
    'decreased_motivation': True,
    'withdrawing_from_people': False,
    'mood_swings': True,
    'black_and_white_thinking': False,
    'negative_thinking': True,
    'change_in_weight_or_appetite': False,
    'change_in_sleeping_pattern': True,
    'suicidal_thoughts_or_plans': False,
    'self_harm': True,
    'homicidal_thoughts_or_plans': False,
    'difficulty_focusing': True,
    'feelings_of_hopelessness': False,
    'feelings_of_shame_or_guilt': True,
    'feelings_of_inadequacy': False,
    'anxious_nervous_tense_feelings': False,
    'panic_attacks': True,
    'racing_or_scrambled_thoughts': False,
    'bad_or_unwanted_thoughts': True,
    'flashbacks_or_nightmares': False,
    'muscle_tensions_aches': True,
    'hearing_voices_or_seeing_things': False,
    'thoughts_of_running_away': True,
    'paranoid_thoughts': False,
    'feelings_of_frustration': True,
    'feelings_of_being_cheated': False,
    'perfectionism': True,
    'counting_washing_checking': False,
    'distorted_body_image': True,
    'concerns_about_dieting': False,
    'loss_of_control_over_eating': True,
    'binge_eating_or_purging': False,
    'rules_about_eating': True,
    'compensating_for_eating': False,
    'excessive_exercise': True,
    'indecisiveness_about_career': False,
    'job_problems': True,
    'other_history': 'No other history',
    'previous_treatments': True,
    'previous_treatments_likes_dislikes': 'Liked the group therapy sessions',
    'previous_treatments_learned': 'Learned coping mechanisms',
    'previous_treatments_like_to_continue': True,
    'previous_hospital_stays_psych': True,
    'current_thoughts_to_harm': False,
    'past_thoughts_to_harm': True,
    'medication_and_dose': 'Zoloft 50mg daily',
    'serious_ch_illnesses_history': 'None',
    'head_injuries': True,
    'lose_consciousness': False,
    'convulsions_or_seizures': True,
    'fever': False,
    'allergies': 'None',
    'current_physical_health': 'Good',
    'last_check_up': '2023-10-15',
    'has_physician': True,
    'physician_name': 'Dr. Johnson',
    'physician_email': 'dr.johnson@example.com',
    'physician_number': '555-123-4567',
    'birth_location': 'City, Canada',
    'raised_by': 'Parents',
    'rel_qual_mother': 'Good',
    'rel_qual_father': 'Fair',
    'rel_qual_step_parent': 'Excellent',
    'family_abuse_history': 'No',
    'family_mental_history': 'Yes',
    'additional_information_family': 'Family history of depression',
    'relationship_with_peers': 'Good',
    'social_support_network': 'Strong',
    'hobbies_or_interests': 'Painting, Yoga',
    'cultural_concerns': 'None',
    'educational_history': 'Psychology',
    'highest_level_achieved': 'Bachelor\'s Degree',
    'additional_information_education': 'Member of the Psychology Club',
    'employment_status': 'Employed',
    'satisfaction': 'Satisfied',
    'satisfaction_reason': 'Enjoying the work environment',
    'struggled_with_substance_abuse': True,

    'alcohol': True,
    'alcohol_age_first_use': 18,
    'alcohol_frequency_of_use': 'Occasionally',
    'alcohol_amount_used': 'Moderate',
    'alcohol_way_of_intake': 'Drinking',

    'cigarette': True,
    'cigarette_age_first_use': 16,
    'cigarette_frequency_of_use': 'Daily',
    'cigarette_amount_used': 'Heavy',
    'cigarette_way_of_intake': 'Smoking',
    
    'marijuana': True,
    'marijuana_age_first_use': 16,
    'marijuana_frequency_of_use': 'Daily',
    'marijuana_amount_used': 'Heavy',
    'marijuana_way_of_intake': 'Smoking',

    'cocaine': True,
    'cocaine_age_first_use': 16,
    'cocaine_frequency_of_use': 'Daily',
    'cocaine_amount_used': 'Heavy',
    'cocaine_way_of_intake': 'Smoking',

    'heroin': True,
    'heroin_age_first_use': 16,
    'heroin_frequency_of_use': 'Daily',
    'heroin_amount_used': 'Heavy',
    'heroin_way_of_intake': 'Smoking',

    'amphetamines': True,
    'amphetamines_age_first_use': 16,
    'amphetamines_frequency_of_use': 'Daily',
    'amphetamines_amount_used': 'Heavy',
    'amphetamines_way_of_intake': 'Smoking',

    'club_drugs': True,
    'club_drugs_age_first_use': 16,
    'club_drugs_frequency_of_use': 'Daily',
    'club_drugs_amount_used': 'Heavy',
    'club_drugs_way_of_intake': 'Smoking',

    'pain_meds': True,
    'pain_meds_age_first_use': 16,
    'pain_meds_frequency_of_use': 'Daily',
    'pain_meds_amount_used': 'Heavy',
    'pain_meds_way_of_intake': 'Smoking',

    'benzo': True,
    'benzo_age_first_use': 16,
    'benzo_frequency_of_use': 'Daily',
    'benzo_amount_used': 'Heavy',
    'benzo_way_of_intake': 'Smoking',

    'other_meds': True,
    'other_meds_age_first_use': 16,
    'other_meds_frequency_of_use': 'Daily',
    'other_meds_amount_used': 'Heavy',
    'other_meds_way_of_intake': 'Smoking',

    'treatment_program_name' : 'form.treatment_program_name.data',
    'treatment_type' : 'Test',
    'treatment_date' : '1999-05-15',
    'treatment_outcome' : 'Test',

    # Include similar fields for other substances
    'pending_criminal_charges': False,
    'on_probation': False,
    'has_been_arrested': False,
    'to_work_on': 'Managing stress',
    'expectations': 'To improve mental well-being',
    'things_to_change': 'Better coping mechanisms',
    'other_information': 'None',
    }

    with app.test_client() as client:

        print(form_data)

        response = client.post('/add', data=form_data, follow_redirects=True)

        print(response)
        print(response.data)

        # Check if the response is successful (status code 200)
        assert response.status_code == 200, "Unexpected status code"

        new_student = BasicInformation.query.filter_by(student_id=form_data['student_id']).first()
        assert new_student is not None

        # Clean up - delete the newly added record from the database
        db.session.delete(new_student)
        db.session.commit()

if __name__ == '__main__':
    pytest.main()