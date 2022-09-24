from website import db
from main import app

db.create_all(app=app)
