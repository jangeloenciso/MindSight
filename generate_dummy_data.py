# Generates 200 dummy records for testing

import random
from datetime import date, timedelta
from faker import Faker
from app import db, app
from app.models.models import *
from dummy_data_input import course_names, religion_names, strands

with app.app_context():

    db.session.query(PersonalInformation).delete()
    db.session.query(FamilyBackground).delete()
    db.session.query(HealthInformation).delete()
    db.session.query(EducationalBackground).delete()
    db.session.query(StudentVisits).delete()
    db.session.query(HistoryInformation).delete()
    db.session.query(SocialHistory).delete()
    db.session.query(OccupationalHistory).delete()
    db.session.query(SubstanceAbuseHistory).delete()
    db.session.query(LegalHistory).delete()
    db.session.query(AdditionalInformation).delete()
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

    def generate_fake_student_visit(student):
        visit = StudentVisits(
            student=student,
            date_of_visit=random_date(date(2020, 1, 1), date(2023, 12, 31)),
            nature_of_concern=fake.random_element(elements=["Academic", "Career", "Personal", "Social"])
        )
        db.session.add(visit)

    for _ in range(200):
        family_name = fake.last_name()
        student = StudentInformation(
            student_id=generate_student_id(),
            last_name=family_name,
            first_name=fake.first_name(),
            course=fake.random_element(elements=course_names),
            year_level=str(random.randint(1, 4)),
            # gpa=round(random.uniform(1.0, 5.0), 2),
            campus=fake.random_element(elements=["Boni", "Pasig"])
        )

        db.session.add(student)
        db.session.commit()

        personal_information = PersonalInformation(
            age=random.randint(18, 30),
            sex=fake.random_element(elements=("Male", "Female")),
            gender=fake.random_element(elements=("Male", "Female", "LGBTQ")),
            contact_number=fake.random_int(min=100000, max=99999999999),
            religion=fake.random_element(elements=religion_names),
            date_of_birth=random_date(date(1990, 1, 1), date(2005, 1, 1)),
            place_of_birth=fake.city(),
            nationality=fake.random_element(elements=("Filipino", "Non-Filipino")),
            counseling_history=fake.random_element(elements=("Yes", "No")),
            residence=fake.random_element(elements=("Family Home", "Guardian's Home", "School Dormitory", "Dormitory", "Others")),
            civil_status=fake.random_element(elements=("Single", "Married", "Divorced", "Widowed")),
            student=student
        )

        history_information = HistoryInformation(
            information_provider=fake.name(),
            current_problem=fake.sentence(),
            problem_length=fake.sentence(),
            stressors=fake.sentence(),
            substance_abuse=fake.boolean(),
            addiction=fake.boolean(),
            depression_sad_down_feelings=fake.boolean(),
            high_low_energy_level=fake.boolean(),
            angry_irritable=fake.boolean(),
            loss_of_interest=fake.boolean(),
            difficulty_enjoying_things=fake.boolean(),
            crying_spells=fake.boolean(),
            decreased_motivation=fake.boolean(),
            withdrawing_from_people=fake.boolean(),
            mood_swings=fake.boolean(),
            black_and_white_thinking=fake.boolean(),
            negative_thinking=fake.boolean(),
            change_in_weight_or_appetite=fake.boolean(),
            change_in_sleeping_pattern=fake.boolean(),
            suicidal_thoughts_or_plans=fake.boolean(),
            self_harm=fake.boolean(),
            homicidal_thoughts_or_plans=fake.boolean(),
            difficulty_focusing=fake.boolean(),
            feelings_of_hopelessness=fake.boolean(),
            feelings_of_shame_or_guilt=fake.boolean(),
            feelings_of_inadequacy=fake.boolean(),
            low_self_esteem=fake.boolean(),
            anxious_nervous_tense_feelings=fake.boolean(),
            panic_attacks=fake.boolean(),
            racing_or_scrambled_thoughts=fake.boolean(),
            bad_or_unwanted_thoughts=fake.boolean(),
            flashbacks_or_nightmares=fake.boolean(),
            muscle_tensions_aches=fake.boolean(),
            hearing_voices_or_seeing_things=fake.boolean(),
            thoughts_of_running_away=fake.boolean(),
            paranoid_thoughts=fake.boolean(),
            feelings_of_frustration=fake.boolean(),
            feelings_of_being_cheated=fake.boolean(),
            perfectionism=fake.boolean(),
            counting_washing_checking=fake.boolean(),
            distorted_body_image=fake.boolean(),
            concerns_about_dieting=fake.boolean(),
            loss_of_control_over_eating=fake.boolean(),
            binge_eating_or_purging=fake.boolean(),
            rules_about_eating=fake.boolean(),
            compensating_for_eating=fake.boolean(),
            excessive_exercise=fake.boolean(),
            indecisiveness_about_career=fake.boolean(),
            job_problems=fake.boolean(),
            other=fake.sentence(),
            previous_treatments=fake.boolean(),
            previous_treatments_likes_dislikes=fake.sentence(),
            previous_treatments_learned=fake.sentence(),
            previous_treatments_like_to_continue=fake.sentence(),
            previous_hospital_stays_psych=fake.boolean(),
            current_thoughts_to_harm=fake.boolean(),
            past_thoughts_to_harm=fake.boolean(),
            student_id=student.student_id
        )

        health_information = HealthInformation(
            medication_and_dose=fake.sentence(),
            serious_ch_illnesses_history=fake.sentence(),
            head_injuries=fake.boolean(),
            lose_consciousness=fake.boolean(),
            convulsions_or_seizures=fake.boolean(),
            fever=fake.boolean(),
            allergies=fake.sentence(),
            current_physical_health=fake.sentence(nb_words=1),
            last_check_up=random_date(date(2020, 1, 1), date(2023, 12, 31)),
            has_physician=fake.boolean(),
            physician_name=fake.name(),
            physician_email=fake.email(),
            physician_number = fake.random_int(min=100000, max=99999999999),
            student=student
        )

        family_background = FamilyBackground(
            father_age=random.randint(35, 60),
            mother_age=random.randint(35, 60),
            father_first_name=fake.first_name(),
            father_last_name=family_name,
            mother_first_name=fake.first_name(),
            mother_last_name=family_name,
            family_abuse_history=fake.sentence(),
            family_mental_history=fake.sentence(),
            additional_information=fake.sentence(),
            student=student
        )

        social_history = SocialHistory(
            relationship_with_peers=fake.sentence(),
            social_support_network=fake.sentence(),
            hobbies_or_interests=fake.sentence(),
            cultural_concerns=fake.sentence(),
            student = student
        )

        educational_background = EducationalBackground(
            educational_history=fake.sentence(),
            highest_level_achieved=fake.sentence(),
            additional_information=fake.sentence(),
            student=student
        )

        occupational_history = OccupationalHistory(
            employment_status=fake.sentence(),
            satisfaction=fake.sentence(),
            satisfaction_reason=fake.sentence(),
            student = student
        )

        substance_abuse_history = SubstanceAbuseHistory(
            struggled_with_substance_abuse=fake.boolean(),
            alcohol=fake.boolean(),
            alcohol_age_first_use = fake.sentence(nb_words=2),
            alcohol_frequency_of_use = fake.sentence(nb_words=2),
            alcohol_amount_used = fake.sentence(nb_words=2),
            alcohol_way_of_intake = fake.sentence(nb_words=2),
            cigarette = fake.boolean(),
            cigarette_age_first_use = fake.sentence(nb_words=2),
            cigarette_frequency_of_use = fake.sentence(nb_words=2),
            cigarette_amount_used = fake.sentence(nb_words=2),
            cigarette_way_of_intake = fake.sentence(nb_words=2),
            marijuana = fake.boolean(),
            marijuana_age_first_use = fake.sentence(nb_words=2),
            marijuana_frequency_of_use = fake.sentence(nb_words=2),
            marijuana_amount_used = fake.sentence(nb_words=2),
            marijuana_way_of_intake = fake.sentence(nb_words=2),
            cocaine = fake.boolean(),
            cocaine_age_first_use = fake.sentence(nb_words=2),
            cocaine_frequency_of_use = fake.sentence(nb_words=2),
            cocaine_amount_used = fake.sentence(nb_words=2),
            cocaine_way_of_intake = fake.sentence(nb_words=2),
            heroin = fake.boolean(),
            heroin_age_first_use = fake.sentence(nb_words=2),
            heroin_frequency_of_use = fake.sentence(nb_words=2),
            heroin_amount_used = fake.sentence(nb_words=2),
            heroin_way_of_intake = fake.sentence(nb_words=2),
            amphetamines = fake.boolean(),
            amphetamines_age_first_use = fake.sentence(nb_words=2),
            amphetamines_frequency_of_use = fake.sentence(nb_words=2),
            amphetamines_amount_used = fake.sentence(nb_words=2),
            amphetamines_way_of_intake = fake.sentence(nb_words=2),
            club_drugs = fake.boolean(),
            club_drugs_age_first_use = fake.sentence(nb_words=2),
            club_drugs_frequency_of_use = fake.sentence(nb_words=2),
            club_drugs_amount_used = fake.sentence(nb_words=2),
            club_drugs_way_of_intake = fake.sentence(nb_words=2),
            pain_meds = fake.boolean(),
            pain_meds_age_first_use = fake.sentence(nb_words=2),
            pain_meds_frequency_of_use = fake.sentence(nb_words=2),
            pain_meds_amount_used = fake.sentence(nb_words=2),
            pain_meds_way_of_intake = fake.sentence(nb_words=2),
            benzo = fake.boolean(),
            benzo_meds_age_first_use = fake.sentence(nb_words=2),
            benzo_meds_frequency_of_use = fake.sentence(nb_words=2),
            benzo_meds_amount_used = fake.sentence(nb_words=2),
            benzo_meds_way_of_intake = fake.sentence(nb_words=2),
            hallucinogens = fake.boolean(),
            hallucinogens_meds_age_first_use = fake.sentence(nb_words=2),
            hallucinogens_meds_frequency_of_use = fake.sentence(nb_words=2),
            hallucinogens_meds_amount_used = fake.sentence(nb_words=2),
            hallucinogens_meds_way_of_intake = fake.sentence(nb_words=2),
            other = fake.boolean(),
            other_meds_age_first_use = fake.sentence(nb_words=2),
            other_meds_frequency_of_use = fake.sentence(nb_words=2),
            other_meds_amount_used = fake.sentence(nb_words=2),
            other_meds_way_of_intake = fake.sentence(nb_words=2),


            student = student
        )

        legal_history = LegalHistory(
            pending_criminal_charges=fake.boolean(),
            on_probation=fake.boolean(),
            has_been_arrested=fake.boolean(),
            student = student
        )

        additional_information = AdditionalInformation(
            to_work_on=fake.sentence(),
            expectations=fake.sentence(),
            things_to_change=fake.sentence(),
            other_information=fake.sentence(),
            student = student
        )

        for _ in range(1):
            generate_fake_student_visit(student)

        db.session.add(personal_information)
        db.session.add(history_information)
        db.session.add(health_information)
        db.session.add(family_background)
        db.session.add(social_history)
        db.session.add(educational_background)
        db.session.add(occupational_history)
        db.session.add(substance_abuse_history)
        db.session.add(legal_history)
        db.session.add(additional_information)

        db.session.commit()

    db.session.close()
