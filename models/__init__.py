from flask_mongoengine import MongoEngine
db = MongoEngine()

def init_app(app):
    """Init app."""
    db.init_app(app)
