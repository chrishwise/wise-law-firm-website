from main import app
from website import db
from website.models import Attorney, AttorneyMembership, AttorneyPublication, AttorneyAreaOfPractice, \
    AttorneyEducation, AttorneyProfessionalLicense, AttorneyAdmission, AttorneyProfessionalActivity

'''Deletes all of the attorney helper tables as well as the Attorney table before recreating them all'''
with app.app_context():
    AttorneyMembership.__table__.drop(db.engine)
    AttorneyPublication.__table__.drop(db.engine)
    AttorneyAreaOfPractice.__table__.drop(db.engine)
    AttorneyEducation.__table__.drop(db.engine)
    AttorneyProfessionalActivity.__table__.drop(db.engine)
    AttorneyProfessionalLicense.__table__.drop(db.engine)
    AttorneyAdmission.__table__.drop(db.engine)
    Attorney.__table__.drop(db.engine)
    db.create_all()
