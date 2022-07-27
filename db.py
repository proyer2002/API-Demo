from app import app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)


@app.before_first_request
def create_database():
    db.create_all()
