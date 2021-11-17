from flask.views import MethodView
from models.user import User
from http import HTTPStatus
from flask import abort

class UserMongoResource(MethodView):
    """Object resource car."""

    def get_all(self):
        """Method to get all users."""

        """
        to-do: pagination
        """
        return User.objects.all()

    def get_by_username(self, username):
        return User.objects(username=username).first()

    def create(self, data):
        user = User()
        for k, v in data.items():
            setattr(user, k, v)
        try:
            user.save()
        except ValidationError as e:
            return abort(HTTPStatus.BAD_REQUEST, e.to_dict())

        return user