import datetime

from flask_wtf import RecaptchaField, FlaskForm
from wtforms import StringField, validators, EmailField, TextAreaField, DateField


class ContactForm(FlaskForm):
    name = StringField('First and Last Name', [validators.InputRequired()],
                       description="Enter your first and last name")
    email = EmailField('Email Address', [validators.InputRequired()])
    message = TextAreaField('Message', [validators.InputRequired()])
    recaptcha = RecaptchaField()


class ArticleForm(FlaskForm):
    title = StringField('Article Title', [validators.InputRequired()])
    text = TextAreaField('Article Content', [validators.InputRequired()])
    publishing_date = DateField('Date of Publishing')
    date_created = datetime.datetime.now()
