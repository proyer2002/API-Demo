from db import db
import psycopg2

class ClientModel(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(80))
    msanum = db.Column(db.Integer)
    url = db.Column(db.String(80))
    create_date = db.Column(db.String(80))
    client_info = db.Column(db.String(80))
    #new_client = db.Column(db.String(80))
   
    def __init__(self, client_name, msanum, url, create_date, client_info):
        self.client_name = client_name
        self.msanum = msanum
        self.url = url
        self.create_date = create_date
        self.client_info = client_info
        #self.new_client = new_client

    def json(self):
        return {
        'id:': self.id, 
        'client_name': self.client_name, 
        'msanum': self.msanum,
        'url': self.url, 
        'create_date': self.create_date,
        'client_info': self.client_info
        #'new_client': self.new_client
        }
    
    @classmethod
    def find_by_name(cls, client_name):
        return cls.query.filter_by(client_name=client_name).first()


    @classmethod
    def find_all(cls):
        return cls.query.all()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()