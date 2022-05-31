from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    authenticated = db.Column(db.Boolean, default=False)

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return self.authenticated

    def __repr__(self):
        return f'<User: {self.email}>'


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    text = db.Column(db.String(10000))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('admin.id'))


class Homepage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    #pic1_data = db.Column(db.LargeBinary, nullable=False)  # Actual data, needed for download
    #pic1_rendered = db.Column(db.Text, nullable=False)  # Data to render the pic in browser
    #pic1_location = db.Column(db.String(64))
    pic1_text_large = db.Column(db.String(200))
    pic1_text_small = db.Column(db.Text)
    banner1_text_large = db.Column(db.String(200))
    banner1_text_small = db.Column(db.Text)
    #pic2_data = db.Column(db.LargeBinary, nullable=False)  # Actual data, needed for download
    #pic2_rendered = db.Column(db.Text, nullable=False)  # Data to render the pic in browser
    #pic2_location = db.Column(db.String(64))
    firm_overview_text = db.Column(db.Text)
    carousel1_title = db.Column(db.String(200))
    carousel1_text = db.Column(db.Text)
    carousel2_title = db.Column(db.String(200))
    carousel2_text = db.Column(db.Text)
    #banner1 = db.relationship('Banner1')
    #parallax_pic2 = db.relationship('ParallaxPic2')
    #banner2 = db.relationship('Banner2')
    #practice_area = db.relationship('PracticeArea')
    #carousel = db.relationship('Carousel')


