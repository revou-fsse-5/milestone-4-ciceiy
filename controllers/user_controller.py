from flask import Blueprint, request, jsonify
from models.user_model import User
from extensions import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from bcrypt import hashpw, gensalt, checkpw

user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/user/register', methods=['POST'])
def register_user():
    data = request.json
    hashed_password = hashpw(data['password'].encode('utf-8'), gensalt())
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=hashed_password.decode('utf-8')
    )
    db.session.add(new_user)
    db.session.commit()
    return {"message": "User registered"}, 201

@user_controller.route('/user/login', methods=['POST'])
def login_user():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and checkpw(data['password'].encode('utf-8'), user.password_hash.encode('utf-8')):
        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, 200
    else:
        return {"message": "Invalid credentials"}, 401

@user_controller.route('/user/me', methods=['GET'])
@jwt_required()
def get_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return {"username": user.username, "email": user.email}, 200

@user_controller.route('/user/me', methods=['PUT'])
@jwt_required()
def update_user():
    current_user_id = get_jwt_identity()
    data = request.json
    user = User.query.get(current_user_id)
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    db.session.commit()
    return {"message": "User updated"}, 200