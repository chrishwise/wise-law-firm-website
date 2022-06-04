from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


#DATABASE_URI = 'postgres://wjaehhgjglwidl:af553f7e379ca0bc017eed1ca195478f62c64f6b368e341319050c283c721545@ec2-52-204-195-41.compute-1.amazonaws.com:5432/d6p2k5p1mmqh7o'
db = SQLAlchemy()
DB_NAME = "database.db"
mail = Mail()
#engine = create_engine(DATABASE_URI)
#Session = sessionmaker(bind=engine)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{DB_NAME}' ,

        # 'postgres://wjaehhgjglwidl:af553f7e379ca0bc017eed1ca195478f62c64f6b368e341319050c283c721545@ec2-52-204-195-41.compute-1.amazonaws.com:5432/d6p2k5p1mmqh7o',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        MAIL_SERVER='smtp.office365.com',
        MAIL_PORT='587',
        MAIL_USE_TLS=True,
        MAIL_USE_SSL=False,
        MAIL_USERNAME="no-reply-wiselawfirm@outlook.com",
        MAIL_PASSWORD="MwWGAMsnRY8!"
    )

    # initialize app with database and Flask-Mail
    db.init_app(app)
    mail.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Admin, Article

    # db.create_all(app=app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.admin'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Admin.query.get(int(id))
    return app







