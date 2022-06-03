from . import db
from flask_login import UserMixin


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



