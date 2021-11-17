
  
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId

import models

from models.user import User

app = Flask(__name__)

app.config['MONGODB_DB'] = 'test'
app.config['MONGODB_HOST'] = 'host.docker.internal'
app.config['MONGODB_PORT'] = 27017

app.config["JWT_SECRET_KEY"] = "shhhh-super-secret"  
jwt = JWTManager(app)

# Init model
models.init_app(app)

"""
to-do: every hour user can trigger one action
to-do: send email every hour (?
"""

@app.route('/')
def hello_world():
    return "Hello world!"

@app.route('/protected', methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(current_user_id)).first()
    if not user:
        return 'invalid token', 403
    print(user)
    return jsonify({"id": str(user.id), "username": user.username}), 200    

@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    username = data.get('username')
    
    if not username:
        return 'missing params', 400
    
    password = data.get('password')
    if not password:
        return 'missing params', 400

    user = User.objects(username=username,password=password).first()
    if not user:
        return 'wrong credentials', 403

    access_token = create_access_token(identity=str(user.id))
    return jsonify({ "token": access_token, "user_id": str(user.id)})

@app.route('/users')
def users():

    collection = User.objects

    item = {}
    data = []
    for element in collection:
        item = {
            'id': str(element.id),
            'username': element.username,
            'created_at': element.created_at,
            'updated_at': element.updated_at
        }
        data.append(item)

    return jsonify(
        data=data
    )

@app.route('/user', methods=['POST'])
def user():
    data = request.json
    username = data.get('username')
    
    if not username:
        return 'missing params', 400
    
    password = data.get('password')
    if not password:
        return 'missing params', 400

    user = User.objects(username=username).first()
    if user:
        return 'username already exists', 403
        
    user = User()
    setattr(user, 'username', username)
    setattr(user, 'password', password)
    setattr(user, 'created_at', datetime.utcnow())
    setattr(user, 'updated_at', datetime.utcnow())

    try:
        user.save()
    except ValidationError as e:
        return abort(HTTPStatus.BAD_REQUEST, e.to_dict())

    """
    to-do: Do not store plain text password
    """

    return 'Saved!', 201

@app.route('/delete-all-users', methods=['POST'])
def delete_all_users():   
    User.objects.delete()
    return 'deleted!', 201    