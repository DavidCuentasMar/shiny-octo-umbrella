
  
from flask import Flask, jsonify, request
from datetime import datetime
from pymongo import MongoClient
app = Flask(__name__)

client = MongoClient('mongodb://mongodb:27017/')
db = client.test_database

@app.route('/')
def hello_world():
    return "Hello world!"

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
        return 'missing params', 403
    
    password = data.get('password')
    if not password:
        return 'missing params', 403

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