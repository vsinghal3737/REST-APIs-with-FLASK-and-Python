from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp as strcmp
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt
)
from models.user import UserModel
from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True, help="This field cannot be left black!")
_user_parser.add_argument('password', type=str, required=True, help="This field cannot be left black!")


class UserRegister(Resource):
    def post(self):

        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "Username Already Exists."}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User Created successfully."}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()
        return {'message': 'user not found'}, 404

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return {"message": "User deleted successfully."}, 200
        return {'message': 'user not found'}, 404


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        """ this is similar to authenticate() function used to do in security.py"""
        if user and strcmp(user.password, data['password']):

            """ this is simlar to identity() function used to do in security.py"""
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {'access_token': access_token, 'refresh_token': refresh_token}, 200

        return {'message': 'invalid username or password'}, 401


class UserList(Resource):

    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'mesasge': 'admin user only'}, 401
        return {'Users': [x.json() for x in UserModel.find_all()]}


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']  # jti is "JWT ID", a unique identifier for a JWT
        BLACKLIST.add(jti)
        return {'message': 'successfully logged out'}


class TokenRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
