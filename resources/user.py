from werkzeug.security import safe_str_cmp
from flask_restful import Resource, reqparse
from blacklist import BLACKLIST
from models.user import UserModel
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt
)
from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be left blank!"
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be left blank!"
                          )
_user_parser.add_argument('in_user',
                          type=int,
                          required=True,
                          help="Please enter 1 or 0 to select if MSA numbers are in use!"
                          )


class UserRegister(Resource):
    TABLE_NAME = 'users'

    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class User(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found!'}, 404
        return user.json()

    @classmethod
    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found!'}, 404
        user.delete_from_db()
        return {'message': 'User successfully deleted!'}, 200


class UserLogin(Resource):

    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()

        # find user in database
        user = UserModel.find_by_username(data['username'])

        # check password (authenticate func)
        if user and safe_str_cmp(user.password, data['password']):
            # identity func
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return{
                'access_token': access_token,
                'refresh_token': refresh_token

            }, 200

        return {'message': 'Invalid credentials!'}, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        sub = get_jwt()['sub']
        BLACKLIST.add(sub)
        return {'message': 'Successfully logged out!'}, 200


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access token': new_token}, 200
