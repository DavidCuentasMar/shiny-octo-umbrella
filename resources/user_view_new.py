from flask import jsonify, request
from resources.user_mongo_resource import UserMongoResource
from datetime import datetime

class UserViewNew(UserMongoResource):
    """Object support api by list."""
    def post(self):
        data = request.json
        username = data.get('username')
        
        if not username:
            return 'missing params', 400
        
        password = data.get('password')
        if not password:
            return 'missing params', 400

        user = self.get_by_username(username)
        if user:
            return 'username already exists', 403
        
        data = {
            'username': username,
            'password': password,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }

        user_created = self.create(data)
        
        """
        to-do: Do not store plain text password
        """

        return 'Saved!', 201