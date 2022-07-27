from app import app
from db import db

db.init_app(app)

db.create_all()
