from re import I
from flask_mongoengine import MongoEngine
from nomenclate_api.config import MONGO_URI

db = MongoEngine()


def init_mongo(app):
    uri = MONGO_URI
    if uri == "undefined":
        uri = "mongodb://localhost:27017/nomenclate-api"
    app.config["MONGODB_SETTINGS"] = {"host": uri}

    db.init_app(app)

    with app.app_context():
        print(f"Connecting to DB: {uri}")
        print(f"Connection state: {db.connection}")
