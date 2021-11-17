from flask import jsonify
from resources.user_mongo_resource import UserMongoResource

class UserViewList(UserMongoResource):
    """Object support api by list."""
    def get(self):
        collection = self.get_all()
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