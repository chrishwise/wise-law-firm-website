from main import app
from website import db
from website.models import Attorney


with app.app_context():

    Attorney.__table__.drop(db.engine)
    db.create_all()
