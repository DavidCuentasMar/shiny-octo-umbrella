
  
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient('mongodb://mongodb:27017/')
db = client.test_database

app.config["JWT_SECRET_KEY"] = "shhhh-super-secret"  
jwt = JWTManager(app)

@app.route('/')
def hello_world():
    return "Hello world!"

@app.route('/protected', methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = db.users.find_one({"_id" :ObjectId(current_user_id)})
    if not user:
        return 'invalid token', 403
    return jsonify({"id": str(user.get('_id')), "username": user.get('username')}), 200    

@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    username = data.get('username')
    
    if not username:
        return 'missing params', 400
    
    password = data.get('password')
    if not password:
        return 'missing params', 400

    user = db.users.find_one(
        {
            'username':username,
            'password':password
        }
    )
    if not user:
        return 'wrong credentials', 403

    access_token = create_access_token(identity=str(user.get('_id')))
    return jsonify({ "token": access_token, "user_id": str(user.get('_id') )})

@app.route('/users')
def users():
    collection = db.users.find()

    item = {}
    data = []
    for element in collection:
        item = {
            'id': str(element['_id']),
            'username': element['username'],
            'created_at': element['created_at'],
            'updated_at': element['updated_at']
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

    user = db.users.find_one({'username':username})
    if user:
        return 'username already exists', 403
        
    now = datetime.now()
    user = {
        'username': username,
        'password': password,
        'created_at': now,
        'updated_at': now
    }

    """
    to-do: Do not store plain text password
    """

    db.users.insert_one(user)

    return 'Saved!', 201

@app.route('/delete-all-users', methods=['POST'])
def delete_all_users():   
    db.users.remove()
    return 'deleted!', 201    