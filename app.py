
  
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from pymongo import MongoClient
from bson.objectid import ObjectId

import models
import resources

from models.user import User

app = Flask(__name__)

app.config['MONGODB_DB'] = 'test'
app.config['MONGODB_HOST'] = 'host.docker.internal'
app.config['MONGODB_PORT'] = 27017
app.config["JWT_SECRET_KEY"] = "shhhh-super-secret"  
jwt = JWTManager(app)

# Init model
models.init_app(app)

# Init resources
resources.init_app(app)

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


@app.route('/delete-all-users', methods=['POST'])
def delete_all_users():   
    User.objects.delete()
    return 'deleted!', 201    