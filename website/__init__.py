import os

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
mail = Mail()


def create_app():
    """Creates the Flask application object and defines its configuration"""
    app = Flask(__name__, instance_relative_config=True)
    # Programatically create databaseURL from env variables for AWS RDS database
    databaseURL = f"postgresql://{os.environ.get('RDS_USERNAME')}:{os.environ.get('RDS_PASSWORD')}@{os.environ.get('RDS_HOSTNAME')}:{os.environ.get('RDS_PORT')}/ebdb"  #ebdb is RDS_DB_NAME environ variable in AWS environment

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=databaseURL,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        MAIL_SERVER='smtp.office365.com',
        MAIL_PORT='587',
        MAIL_USE_TLS=True,
        MAIL_USE_SSL=False,
        MAIL_USERNAME="no-reply-wiselawfirm@outlook.com",
        MAIL_DEFAULT_SENDER="no-reply-wiselawfirm@outlook.com",
        MAIL_PASSWORD="MwWGAMsnRY8!",
        RECAPTCHA_PUBLIC_KEY=os.environ.get('RECAPTCHA_PUBLIC_KEY'),
        RECAPTCHA_PRIVATE_KEY=os.environ.get('RECAPTCHA_PRIVATE_KEY')
    )

    # initialize app with database and Flask-Mail
    db.init_app(app)
    mail.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Admin, Article   # Employee, ProfessionalLicense, ProfessionalActivity, Education, Publication, Admission, EmployeeAreaOfPractice, Membership

    with app.app_context():
        #db.drop_all()
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.admin_login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Admin.query.get(int(id))

    return app







