# Generates 200 dummy records for testing

import os
import random
from datetime import date, timedelta
from faker import Faker
from app import db, app
from app.models.models import *
from dummy_data_input import *

with app.app_context():

    # db.session.query(PersonalInformation).delete()
    db.session.query(Sibling).delete()
    db.session.query(Conviction).delete()
    db.session.query(CaseNote).delete()
    db.session.query(ReferralInformation).delete()
    db.session.query(FamilyBackground).delete()
    db.session.query(HealthInformation).delete()
    db.session.query(EducationalBackground).delete()
    db.session.query(Sessions).delete()
    db.session.query(HistoryInformation).delete()
    db.session.query(SocialHistory).delete()
    db.session.query(OccupationalHistory).delete()
    db.session.query(SubstanceAbuseHistory).delete()
    db.session.query(LegalHistory).delete()
    db.session.query(AdditionalInformation).delete()
    db.session.query(Document).delete()
    db.session.query(BasicInformation).delete()
    db.session.commit()

    db.session.close()
