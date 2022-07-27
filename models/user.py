import psycopg2
from db import db


class UserModel(db.Model):
    __tablename__ = 'users'
    #TABLE_NAME = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    in_user = db.Column(db.Integer)

    def __init__(self, username, password, in_user):
        self.username = username
        self.password = password
        self.in_user = in_user

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'in_user': self.in_user
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
