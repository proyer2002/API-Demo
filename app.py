# Phoebe Royer Summer 2022 Reveal Data

from venv import create
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from requests import session
from sqlalchemy import create_engine


from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.client import Client, ClientList
from blacklist import BLACKLIST

from db import db

import sys

app = Flask(__name__)
db.init_app(app)

# Database Connection
try:
    conn = "postgresql://revealdata:H0th15C0ld!!@mastermsa-db-001.cidxb3vnerlr.us-east-1.rds.amazonaws.com:5432/master_msa"
except:
    sys.exit({'message': 'Unable to connect to database!'})


jwt = JWTManager(app)  # auth


# Token validation


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 'revealdata':  # This is hard coded, should be reading from config or database, how to do?
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed!',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def mssing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token!',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'Token is not fresh!',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'Token has been revoked!',
        'error': 'token_revoked'
    }), 401


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


# App configuration
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_IDENTITY_CLAIM'] = 'sub'
app.secret_key = 'phoebe'  # dont put key inside reveal api, here for testing purposes
api = Api(app)

# App resources
api.add_resource(Client, '/client/<string:client_name>')
api.add_resource(ClientList, '/clients')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserRegister, '/register')
api.add_resource(TokenRefresh, '/refresh')


if __name__ == '__main__':  # Main
    db.init_app(app)
    # db.create_all()
    app.run(port=5000, debug=True)
