import datetime

from flask_login import current_user
from flask_wtf import RecaptchaField, FlaskForm
from werkzeug.security import check_password_hash
from wtforms import StringField, validators, EmailField, TextAreaField, DateField, SelectField, PasswordField, \
    ValidationError, HiddenField

from website.models import Admin


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
    url = StringField('Article URL')
    date_added = DateField('Date Added', default=datetime.datetime.now())


class AdminAccountForm(FlaskForm):
    first_name = StringField("First Name", [validators.InputRequired(), validators.Length(min=2, max=20)])
    email = EmailField("Admin Email Address", [validators.InputRequired(), validators.Email()])
    notifications = SelectField("Email Notifications?",
                                coerce=lambda x: x == 'True', choices=[('True', 'Yes'), ('False', 'No')])


class AdminChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', [validators.InputRequired()])
    new_password = PasswordField('New Password', [validators.InputRequired(), validators.Length(min=4, max=20)])
    confirm_password = PasswordField('Confirm New Password',
                                     [validators.InputRequired(), validators.Length(min=4, max=20)])

    def validate_current_password(self, field):
        if not check_password_hash(current_user.password, self.current_password.data):
            raise ValidationError('Current password is not correct')

    def validate_confirm_password(self, field):
        if self.new_password.data != self.confirm_password.data:
            raise ValidationError('Passwords must match')


class MasterPasswordForm(FlaskForm):
    master_password = PasswordField("Master Password", [validators.InputRequired()])

    def validate_master_password(self, field):
        master_password_official = Admin.query.filter_by(email="no-reply-wiselawfirm@outlook.com").first().password
        print(master_password_official)
        print(self.master_password.data)
        print(check_password_hash(master_password_official, self.master_password.data))
        if not check_password_hash(master_password_official, self.master_password.data):
            raise ValidationError('Master Password is not correct')


class AdminLoginForm(FlaskForm):
    email = EmailField('Email', [validators.Email()])
    password = PasswordField('Password', [validators.InputRequired()])


class AdminSignUpForm(FlaskForm):
    first_name = StringField('First Name', [validators.InputRequired()])
    email = EmailField('Email', [validators.Email()])
    password = PasswordField('Password', [validators.InputRequired()])
    confirm_password = PasswordField('Confirm Password', [validators.InputRequired()])
    notifications = SelectField("Email Notifications?",
                                coerce=lambda x: x == 'True', choices=[('True', 'Yes'), ('False', 'No')])

    def validate_email(self, field):
        """Ensure the EmailField in AdminSignUpForm is unique"""
        # print(Admin.query.filter_by(email=self.email.data).first() is not None)
        if Admin.query.filter_by(email=self.email.data).first() is not None:
            raise ValidationError('Email already exists')

    def validate_confirm_password(self, field):
        if self.password.data != self.confirm_password.data:
            raise ValidationError('Passwords must match')


class CreateAttorneyForm(FlaskForm):
    name = StringField('First and Last Name', [validators.InputRequired()])
    title = StringField('Title', [validators.InputRequired()])
    email = EmailField('Email', [validators.Email()])
    phone_number = StringField('Phone Number')
    about = TextAreaField('About')
    picture_url = HiddenField(id='image-url', validators=[validators.InputRequired()])

    professional_licenses = HiddenField()
    professional_activities = HiddenField()
    education = HiddenField()
    publications = HiddenField()
    areas_of_practice = HiddenField()
    admissions = HiddenField()
    memberships = HiddenField()

