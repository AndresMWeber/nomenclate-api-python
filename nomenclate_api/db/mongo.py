import logging
from flask_mongoengine import MongoEngine
from nomenclate_api.config import MONGO_URI

LOG = logging.getLogger("nomenclate-api:mongo")
db = MongoEngine()


def init_mongo(app):
    uri = MONGO_URI
    if uri == "undefined":
        uri = "mongodb://localhost:27017/nomenclate-api"
    app.config["MONGODB_SETTINGS"] = {"host": uri}

    db.init_app(app)

    with app.app_context():
        LOG.info(f"Connecting to DB: {uri}")
        LOG.info(f"Connection state: {db.connection}")
