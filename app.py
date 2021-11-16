
  
from flask import Flask, jsonify, request
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
            'name': element['name'],
            'lastname': element['lastname']
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
        return ' missing params', 403

    user = {
        'username': username,
        'password': password
    }
    """
    to-do: Validate that there's no user with same username
    to-do: Do not store plain text password
    """
    #db.users.insert_one(user)

    return 'Saved!', 201