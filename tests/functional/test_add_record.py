from app import app
from app.models.models import *


def test_add_record():
    # Generate form data for a new student record
    form_data = {
    'student_id': '2023-123456',
    'last_name': 'Doe',
    'first_name': 'John',
    'college_name': 'IHK',
    'course_name': 'Computer Science',
    'year_level': 'Sophomore',
    'campus': 'Main',
    'age': 25,
    'sex': 'Male',
    'gender': 'Male',
    'contact_number': '1234567890',
    'religion': 'Christian',
    'date_of_birth': '1999-05-15',
    'place_of_birth': 'Manila',
    'nationality': 'Filipino',
    'counseling_history': 'Yes',
    'residence': 'Family Home',
    'civil_status': 'Single',
    'information_provider': 'Jane Smith',
    'current_problem': 'Feeling stressed',
    'problem_length': 'Several months',
    'stressors': 'Work pressure',
    'substance_abuse': False,
    'addiction': False,
    'medication_and_dose': 'None',
    'serious_ch_illnesses_history': 'None',
    'head_injuries': False,
    'lose_consciousness': False,
    'convulsions_or_seizures': False,
    'fever': False,
    'allergies': 'None',
    'current_physical_health': 'Good',
    'last_check_up': '2023-01-15',
    'has_physician': True,
    'physician_name': 'Dr. Alex Johnson',
    'physician_email': 'alex.johnson@example.com',
    'physician_number': '9876543210',
    'father_age': 55,
    'mother_age': 50,
    'father_first_name': 'Michael',
    'father_last_name': 'Doe',
    'mother_first_name': 'Emma',
    'mother_last_name': 'Doe',
    'family_abuse_history': 'None',
    'family_mental_history': 'None',
    'additional_information': 'None',
    'relationship_with_peers': 'Good',
    'social_support_network': 'Strong',
    'hobbies_or_interests': 'Reading, playing sports',
    'cultural_concerns': 'None',
    'educational_history': 'High school graduate',
    'highest_level_achieved': 'Bachelor\'s degree',
    'additional_information_edu': 'None',
    'employment_status': 'Employed',
    'satisfaction': 'Satisfied',
    'satisfaction_reason': 'Good working environment',
    'struggled_with_substance_abuse': False,
    'alcohol': False,
    'alcohol_age_first_use': 'N/A',
    'alcohol_frequency_of_use': 'N/A',
    'alcohol_amount_used': 'N/A',
    'alcohol_way_of_intake': 'N/A',
    'cigarette': False,
    'cigarette_age_first_use': 'N/A',
    'cigarette_frequency_of_use': 'N/A',
    'cigarette_amount_used': 'N/A',
    'cigarette_way_of_intake': 'N/A',
    'marijuana': False,
    'marijuana_age_first_use': 'N/A',
    'marijuana_frequency_of_use': 'N/A',
    'marijuana_amount_used': 'N/A',
    'marijuana_way_of_intake': 'N/A',
    'cocaine': False,
    'cocaine_age_first_use': 'N/A',
    'cocaine_frequency_of_use': 'N/A',
    'cocaine_amount_used': 'N/A',
    'cocaine_way_of_intake': 'N/A',
    'heroin': False,
    'heroin_age_first_use': 'N/A',
    'heroin_frequency_of_use': 'N/A',
    'heroin_amount_used': 'N/A',
    'heroin_way_of_intake': 'N/A',
    'amphetamines': False,
    'amphetamines_age_first_use': 'N/A',
    'amphetamines_frequency_of_use': 'N/A',
    'amphetamines_amount_used': 'N/A',
    'amphetamines_way_of_intake': 'N/A',
    'club_drugs': False,
    'club_drugs_age_first_use': 'N/A',
    'club_drugs_frequency_of_use': 'N/A',
    'club_drugs_amount_used': 'N/A',
    'club_drugs_way_of_intake': 'N/A',
    'pain_meds': False,
    'pain_meds_age_first_use': 'N/A',
    'pain_meds_frequency_of_use': 'N/A',
    'pain_meds_amount_used': 'N/A',
    'pain_meds_way_of_intake': 'N/A',
    'benzo': False,
    'benzo_meds_age_first_use': 'N/A',
    'benzo_meds_frequency_of_use': 'N/A',
    'benzo_meds_amount_used': 'N/A',
    'benzo_meds_way_of_intake': 'N/A',
    'hallucinogens': False,
    'hallucinogens_meds_age_first_use': 'N/A',
    'hallucinogens_meds_frequency_of_use': 'N/A',
    'hallucinogens_meds_amount_used': 'N/A',
    'hallucinogens_meds_way_of_intake': 'N/A',
    'other': False,
    'other_meds_age_first_use': 'N/A',
    'other_meds_frequency_of_use': 'N/A',
    'other_meds_amount_used': 'N/A',
    'other_meds_way_of_intake': 'N/A',
    'pending_criminal_charges': False,
    'on_probation': False,
    'has_been_arrested': False,
    'to_work_on': 'Improve study habits',
    'expectations': 'Graduate with honors',
    'things_to_change': 'Manage time better',
    'other_information': 'None',
}




    # Simulate a POST request to the /add route with the generated form data
    with app.test_client() as client:
        response = client.post('/add', data=form_data, follow_redirects=True)

        # Check if the response is successful (status code 200)
        assert response.status_code == 200


        # Check if the success message is displayed
        # assert b'New student record added successfully!' in response.data

        # Check if the new record is added to the database
        new_student = BasicInformation.query.filter_by(student_id=form_data['student_id']).first()
        assert new_student is not None
        assert new_student.last_name == form_data['last_name']
        assert new_student.first_name == form_data['first_name']
        assert new_student.course == form_data['course']
        assert new_student.year_level == form_data['year_level']
        assert new_student.campus == form_data['campus']
        assert new_student.personal_information.age == form_data['age']
        assert new_student.personal_information.sex == form_data['sex']
        assert new_student.personal_information.gender == form_data['gender']
        assert new_student.personal_information.contact_number == form_data['contact_number']
        assert new_student.personal_information.religion == form_data['religion']
        assert new_student.personal_information.date_of_birth == form_data['date_of_birth']
        assert new_student.personal_information.place_of_birth == form_data['place_of_birth']
        assert new_student.personal_information.nationality == form_data['nationality']
        assert new_student.personal_information.counseling_history == form_data['counseling_history']
        assert new_student.personal_information.residence == form_data['residence']
        assert new_student.personal_information.civil_status == form_data['civil_status']
        assert new_student.history_information.information_provider == form_data['information_provider']
        assert new_student.history_information.current_problem == form_data['current_problem']
        assert new_student.history_information.problem_length == form_data['problem_length']
        assert new_student.history_information.stressors == form_data['stressors']
        assert new_student.history_information.substance_abuse == form_data['substance_abuse']
        assert new_student.history_information.addiction == form_data['addiction']
        assert new_student.health_information.medication_and_dose == form_data['medication_and_dose']
        assert new_student.health_information.serious_ch_illnesses_history == form_data['serious_ch_illnesses_history']
        assert new_student.health_information.head_injuries == form_data['head_injuries']
        assert new_student.health_information.lose_consciousness == form_data['lose_consciousness']
        assert new_student.health_information.convulsions_or_seizures == form_data['convulsions_or_seizures']
        assert new_student.health_information.fever == form_data['fever']
        assert new_student.health_information.allergies == form_data['allergies']
        assert new_student.health_information.current_physical_health == form_data['current_physical_health']
        assert new_student.health_information.last_check_up == form_data['last_check_up']
        assert new_student.health_information.has_physician == form_data['has_physician']
        assert new_student.health_information.physician_name == form_data['physician_name']
        assert new_student.health_information.physician_email == form_data['physician_email']
        assert new_student.health_information.physician_number == form_data['physician_number']
        assert new_student.family_background.father_age == form_data['father_age']
        assert new_student.family_background.mother_age == form_data['mother_age']
        assert new_student.family_background.father_first_name == form_data['father_first_name']
        assert new_student.family_background.father_last_name == form_data['father_last_name']
        assert new_student.family_background.mother_first_name == form_data['mother_first_name']
        assert new_student.family_background.mother_last_name == form_data['mother_last_name']
        assert new_student.family_background.family_abuse_history == form_data['family_abuse_history']
        assert new_student.family_background.family_mental_history == form_data['family_mental_history']
        assert new_student.family_background.additional_information == form_data['additional_information']
        assert new_student.social_history.relationship_with_peers == form_data['relationship_with_peers']
        assert new_student.social_history.social_support_network == form_data['social_support_network']
        assert new_student.social_history.hobbies_or_interests == form_data['hobbies_or_interests']
        assert new_student.social_history.cultural_concerns == form_data['cultural_concerns']
        assert new_student.educational_background.educational_history == form_data['educational_history']
        assert new_student.educational_background.highest_level_achieved == form_data['highest_level_achieved']
        assert new_student.educational_background.additional_information == form_data['additional_information_edu']
        assert new_student.occupational_history.employment_status == form_data['employment_status']
        assert new_student.occupational_history.satisfaction == form_data['satisfaction']
        assert new_student.occupational_history.satisfaction_reason == form_data['satisfaction_reason']
        assert new_student.substance_abuse_history.struggled_with_substance_abuse == form_data['struggled_with_substance_abuse']
        assert new_student.substance_abuse_history.alcohol == form_data['alcohol']
        assert new_student.substance_abuse_history.alcohol_age_first_use == form_data['alcohol_age_first_use']
        assert new_student.substance_abuse_history.alcohol_frequency_of_use == form_data['alcohol_frequency_of_use']
        assert new_student.substance_abuse_history.alcohol_amount_used == form_data['alcohol_amount_used']
        assert new_student.substance_abuse_history.alcohol_way_of_intake == form_data['alcohol_way_of_intake']
        assert new_student.substance_abuse_history.cigarette == form_data['cigarette']
        assert new_student.substance_abuse_history.cigarette_age_first_use == form_data['cigarette_age_first_use']
        assert new_student.substance_abuse_history.cigarette_frequency_of_use == form_data['cigarette_frequency_of_use']
        assert new_student.substance_abuse_history.cigarette_amount_used == form_data['cigarette_amount_used']
        assert new_student.substance_abuse_history.cigarette_way_of_intake == form_data['cigarette_way_of_intake']
        assert new_student.substance_abuse_history.marijuana == form_data['marijuana']
        assert new_student.substance_abuse_history.marijuana_age_first_use == form_data['marijuana_age_first_use']
        assert new_student.substance_abuse_history.marijuana_frequency_of_use == form_data['marijuana_frequency_of_use']
        assert new_student.substance_abuse_history.marijuana_amount_used == form_data['marijuana_amount_used']
        assert new_student.substance_abuse_history.marijuana_way_of_intake == form_data['marijuana_way_of_intake']
        assert new_student.substance_abuse_history.cocaine == form_data['cocaine']
        assert new_student.substance_abuse_history.cocaine_age_first_use == form_data['cocaine_age_first_use']
        assert new_student.substance_abuse_history.cocaine_frequency_of_use == form_data['cocaine_frequency_of_use']
        assert new_student.substance_abuse_history.cocaine_amount_used == form_data['cocaine_amount_used']
        assert new_student.substance_abuse_history.cocaine_way_of_intake == form_data['cocaine_way_of_intake']
        assert new_student.substance_abuse_history.heroin == form_data['heroin']
        assert new_student.substance_abuse_history.heroin_age_first_use == form_data['heroin_age_first_use']
        assert new_student.substance_abuse_history.heroin_frequency_of_use == form_data['heroin_frequency_of_use']
        assert new_student.substance_abuse_history.heroin_amount_used == form_data['heroin_amount_used']
        assert new_student.substance_abuse_history.heroin_way_of_intake == form_data['heroin_way_of_intake']
        assert new_student.substance_abuse_history.amphetamines == form_data['amphetamines']
        assert new_student.substance_abuse_history.amphetamines_age_first_use == form_data['amphetamines_age_first_use']
        assert new_student.substance_abuse_history.amphetamines_frequency_of_use == form_data['amphetamines_frequency_of_use']
        assert new_student.substance_abuse_history.amphetamines_amount_used == form_data['amphetamines_amount_used']
        assert new_student.substance_abuse_history.amphetamines_way_of_intake == form_data['amphetamines_way_of_intake']
        assert new_student.substance_abuse_history.club_drugs == form_data['club_drugs']
        assert new_student.substance_abuse_history.club_drugs_age_first_use == form_data['club_drugs_age_first_use']
        assert new_student.substance_abuse_history.club_drugs_frequency_of_use == form_data['club_drugs_frequency_of_use']
        assert new_student.substance_abuse_history.club_drugs_amount_used == form_data['club_drugs_amount_used']
        assert new_student.substance_abuse_history.club_drugs_way_of_intake == form_data['club_drugs_way_of_intake']
        assert new_student.substance_abuse_history.pain_meds == form_data['pain_meds']
        assert new_student.substance_abuse_history.pain_meds_age_first_use == form_data['pain_meds_age_first_use']
        assert new_student.substance_abuse_history.pain_meds_frequency_of_use == form_data['pain_meds_frequency_of_use']
        assert new_student.substance_abuse_history.pain_meds_amount_used == form_data['pain_meds_amount_used']
        assert new_student.substance_abuse_history.pain_meds_way_of_intake == form_data['pain_meds_way_of_intake']
        assert new_student.substance_abuse_history.benzo == form_data['benzo']
        assert new_student.substance_abuse_history.benzo_meds_age_first_use == form_data['benzo_meds_age_first_use']
        assert new_student.substance_abuse_history.benzo_meds_frequency_of_use == form_data['benzo_meds_frequency_of_use']
        assert new_student.substance_abuse_history.benzo_meds_amount_used == form_data['benzo_meds_amount_used']
        assert new_student.substance_abuse_history.benzo_meds_way_of_intake == form_data['benzo_meds_way_of_intake']
        assert new_student.substance_abuse_history.hallucinogens == form_data['hallucinogens']
        assert new_student.substance_abuse_history.hallucinogens_meds_age_first_use == form_data['hallucinogens_meds_age_first_use']
        assert new_student.substance_abuse_history.hallucinogens_meds_frequency_of_use == form_data['hallucinogens_meds_frequency_of_use']
        assert new_student.substance_abuse_history.hallucinogens_meds_amount_used == form_data['hallucinogens_meds_amount_used']
        assert new_student.substance_abuse_history.hallucinogens_meds_way_of_intake == form_data['hallucinogens_meds_way_of_intake']
        assert new_student.substance_abuse_history.other == form_data['other']
        assert new_student.substance_abuse_history.other_meds_age_first_use == form_data['other_meds_age_first_use']
        assert new_student.substance_abuse_history.other_meds_frequency_of_use == form_data['other_meds_frequency_of_use']
        assert new_student.substance_abuse_history.other_meds_amount_used == form_data['other_meds_amount_used']
        assert new_student.substance_abuse_history.other_meds_way_of_intake == form_data['other_meds_way_of_intake']
        assert new_student.legal_history.pending_criminal_charges == form_data['pending_criminal_charges']
        assert new_student.legal_history.on_probation == form_data['on_probation']
        assert new_student.legal_history.has_been_arrested == form_data['has_been_arrested']
        assert new_student.additional_information.to_work_on == form_data['to_work_on']
        assert new_student.additional_information.expectations == form_data['expectations']
        assert new_student.additional_information.things_to_change == form_data['things_to_change']
        assert new_student.additional_information.other_information == form_data['other_information']



        # Clean up - delete the newly added record from the database
        db.session.delete(new_student)
        db.session.commit()

if __name__ == '__main__':
    test_add_record()