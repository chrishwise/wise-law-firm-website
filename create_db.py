from website import db
from main import app

db.drop_all(app=app)
db.create_all(app=app)
