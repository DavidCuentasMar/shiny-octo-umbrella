from models import db

class User(db.Document):
    """Object model user."""
    username = db.StringField(required=True)
    password = db.StringField(required=True)
    created_at = db.DateTimeField(required=True)
    updated_at = db.DateTimeField(required=True)