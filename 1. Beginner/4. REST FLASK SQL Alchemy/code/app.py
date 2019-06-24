# import datetime
from flask import Flask, jsonify
from flask_restful import Api
# from flask_jwt import JWT
from flask_jwt_extended import JWTManager

# from security import authenticate, identity
from db import db
from resources.user import UserRegister, User, UserLogin, UserList, UserLogout, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

# app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=7)
app.secret_key = 'vaibhav'  # app.secret_key = app.config['JWT_SECRET_KEY']

api = Api(app)


@app.before_first_request
def create_table():
    db.create_all()


# jwt = JWT(app, authenticate, identity)  # /auth
jwt = JWTManager(app)  # not creating /auth endpoint

"""
`claims` are data we choose to attach to each jwt payload
and for each jwt protected endpoint, we can retrieve these claims via `get_jwt_claims()`
one possible use case for claims are access level control, which is shown below.
"""


@jwt.user_claims_loader
def add_claims_to_jwt(identity):  # Remember identity is what we define when creating the access token
    if identity == 1:   # instead of hard-coding, we should read from a config file or database to get a list of admins instead
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callblock():
    return jsonify({'description': 'the token has expired', 'error': 'token expired'}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'signature varification failed',
        'error': 'invalid token',
        'message': "Dude!!!, really? Com'on Man"
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked',
        'error': 'token_revoked'
    }), 401


# Resources
api.add_resource(UserLogin, '/login')  # /auth endpoint
api.add_resource(UserLogout, '/logout')  # /auth endpoint


api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1:5000/item/<string:item_name>
# similar to this, @app.route('/student/<string:name>'), but in RESTful form

api.add_resource(ItemList, '/items')

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

# api.add_resource(user, '/user/<int:user_id>')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')

api.add_resource(UserList, '/users')

api.add_resource(TokenRefresh, '/refresh')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
