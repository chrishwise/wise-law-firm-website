import datetime

from sqlalchemy.orm import relationship, backref

from . import db
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.Text())   # needs unlimited length for scrypt hash or it will be truncated
    first_name = db.Column(db.String(150))
    receives_notifications = db.Column(db.Boolean, default=False)
    master_password_authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, email, password, first_name, receives_notifications):
        self.email = email
        self.password = generate_password_hash(password, method='scrypt')
        self.first_name = first_name
        self.receives_notifications = receives_notifications

    def __repr__(self):
        return f'<User: {self.email}>'

    def change_password(self, new_password):
        self.password = new_password

    def replace_name(self,new_name):
        self.first_name = new_name

    def replace_email(self, new_email):
        self.email = new_email

    def sets_notifications(self, wants_notifications):
        self.receives_notifications = wants_notifications

    def set_master_clearance(self):
        self.master_password_authenticated = True

    def remove_master_clearance(self):
        self.master_password_authenticated = False

    def has_master_clearance(self):
        return self.master_password_authenticated


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    text = db.Column(db.Text)
    date = db.Column(db.Date)
    published_date = db.Column(db.Date)
    url = db.Column(db.String())

    def __init__(self, title, text, date=datetime.datetime.now(), published_date=None, url="No Source Provided"):
        self.title = title
        self.text = text
        self.date = date
        self.published_date = published_date
        self.url = url


class AttorneyProfessionalLicense(db.Model):
    """Helper Table for attorneys"""
    __tablename__ = 'professional_license'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))

    # Many-to-one Relationships
    attorney_id = db.Column(db.Integer(), db.ForeignKey('attorney.id', ondelete='CASCADE'))
    attorney = relationship('Attorney', backref=backref('professional_licenses', passive_deletes=True))

    def to_string(self):
        return self.title


class AttorneyProfessionalActivity(db.Model):
    """Helper Table for attorneys"""
    __tablename__ = 'professional_activity'
    id = db.Column(db.Integer, primary_key=True)
    # Many-to-one Relationships
    attorney_id = db.Column(db.Integer(), db.ForeignKey('attorney.id', ondelete='CASCADE'))
    attorney = relationship('Attorney', backref=backref('professional_activities', passive_deletes=True))
    title = db.Column(db.String(200))

    def to_string(self):
        return self.title


class AttorneyEducation(db.Model):
    """Helper Table for attorneys"""
    __tablename__ = 'education'
    id = db.Column(db.Integer, primary_key=True)
    # Many-to-one Relationships
    attorney_id = db.Column(db.Integer(), db.ForeignKey('attorney.id', ondelete='CASCADE'))
    attorney = relationship('Attorney', backref=backref('education', passive_deletes=True))
    degree = db.Column(db.String(200))
    school = db.Column(db.String(200))
    year = db.Column(db.String(10))
    accolades = db.Column(db.String(200), default="")

    def to_string(self):
        if self.accolades != "":
            return self.school + " " + self.year + ", " + self.degree + ", " + self.accolades
        else:
            return self.school + " " + self.year + ", " + self.degree


class AttorneyPublication(db.Model):
    """Helper Table for attorneys"""
    __tablename__ = 'publication'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    details = db.Column(db.String(200))
    publication = db.Column(db.String(200))
    year = db.Column(db.String(10))

    # Many-to-one Relationships
    attorney_id = db.Column(db.Integer(), db.ForeignKey('attorney.id', ondelete='CASCADE'))
    attorney = relationship('Attorney', backref=backref('publications', passive_deletes=True))

    def to_string(self):
        return self.title + ", " + self.details + ", " + self.publication + ", " + self.year


class AttorneyAreaOfPractice(db.Model):
    __tablename__ = 'area_of_practice'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    # Many-to-one Relationships
    attorney_id = db.Column(db.Integer(), db.ForeignKey('attorney.id', ondelete='CASCADE'))
    attorney = relationship('Attorney', backref=backref('areas_of_practice', passive_deletes=True))

    def to_string(self):
        return self.name


class AttorneyAdmission(db.Model):
    """Helper Table for attorneys"""
    __tablename__ = 'admission'
    id = db.Column(db.Integer, primary_key=True)
    court = db.Column(db.String(200))
    year = db.Column(db.String(200))
    # Many-to-one Relationships
    attorney_id = db.Column(db.Integer(), db.ForeignKey('attorney.id', ondelete='CASCADE'))
    attorney = relationship('Attorney', backref=backref('admissions', passive_deletes=True))

    def to_string(self):
        return self.court + ", " + self.year


class AttorneyMembership(db.Model):
    """Helper Table for attorneys"""
    __tablename__ = 'membership'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    # Many-to-one Relationships
    attorney_id = db.Column(db.Integer(), db.ForeignKey('attorney.id', ondelete='CASCADE'))
    attorney = relationship('Attorney', backref=backref('memberships', passive_deletes=True))

    def to_string(self):
        return self.name


class Attorney(db.Model):
    __tablename__ = 'attorney'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    title = db.Column(db.String(200))
    email = db.Column(db.String(200))
    phone_number = db.Column(db.String(15))
    about = db.Column(db.Text())


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime)
    name = db.Column(db.String(150))
    email = db.Column(db.String())
    message = db.Column(db.Text())
    responded = db.Column(db.Boolean)
    archived = db.Column(db.Boolean, default=False)

