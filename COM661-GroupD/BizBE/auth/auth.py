from flask import Blueprint, make_response, jsonify, request
from decorators import jwt_required
import bcrypt
import jwt
import datetime
import globals

users = globals.db.users
blacklist = globals.db.blacklist

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/api/v1.0/login", methods=['GET'])
def login():
    auth = request.authorization

    if auth:
        user = users.find_one({'username': auth.username})

        if user is not None:
            if bcrypt.checkpw(bytes(auth.password, 'utf-8'), user["password"]):
                token = jwt.encode({
                    'user' : auth.username,
                    'admin': user['admin'],
                    'exp' : datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30)
                },
                globals.secret_key,
                algorithm="HS256")

                return make_response(jsonify({"token": token}), 200)

            else:
                return make_response(jsonify({'message':'Bad password'}), 401)
        
        else:
            return make_response(jsonify({'message':'Bad username'}), 401)
    
    return make_response("Could not verify", 401, \
        {'WWW-Authenticate': 'Basic realm = "Login required"'})

@auth_bp.route("/api/v1.0/logout", methods=['GET'])
@jwt_required
def logout():
    token = request.headers['x-access-token']
    blacklist.insert_one({"token":token})

    return make_response(jsonify({'message':'Logout successful'}), 200)