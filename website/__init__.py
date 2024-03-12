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
    # Programatically create database_url from env variables for AWS RDS database
    # database_url = f"postgresql://{os.environ.get('RDS_USERNAME')}:{os.environ.get('RDS_PASSWORD')}@{os.environ.get('RDS_HOSTNAME')}:{os.environ.get('RDS_PORT')}/{os.environ.get('RDS_DB_NAME')}"  #ebdb is RDS_DB_NAME environ variable in AWS environment
    heroku_url = os.environ.get('DATABASE_URL')
    # postgres:// in the heroku_url should be "postgresql://"
    heroku_fixed_url = str(heroku_url).replace("postgres://", "postgresql://", 1)
    database_url = heroku_fixed_url

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=database_url,
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
        #drop_everything()
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.admin_login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Admin.query.get(int(id))

    return app


def drop_everything():
    """(On a live db) drops all foreign key constraints before dropping all tables.
    Workaround for SQLAlchemy not doing DROP ## CASCADE for drop_all()
    (https://github.com/pallets/flask-sqlalchemy/issues/722)
    """
    from sqlalchemy.engine.reflection import Inspector
    from sqlalchemy.schema import DropConstraint, DropTable, MetaData, Table

    con = db.engine.connect()
    trans = con.begin()
    inspector = Inspector.from_engine(db.engine)

    # We need to re-create a minimal metadata with only the required things to
    # successfully emit drop constraints and tables commands for postgres (based
    # on the actual schema of the running instance)
    meta = MetaData()
    tables = []
    all_fkeys = []

    for table_name in inspector.get_table_names():
        fkeys = []

        for fkey in inspector.get_foreign_keys(table_name):
            if not fkey["name"]:
                continue

            fkeys.append(db.ForeignKeyConstraint((), (), name=fkey["name"]))

        tables.append(Table(table_name, meta, *fkeys))
        all_fkeys.extend(fkeys)

    for fkey in all_fkeys:
        con.execute(DropConstraint(fkey))

    for table in tables:
        con.execute(DropTable(table))

    trans.commit()







