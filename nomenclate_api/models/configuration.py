from .config import db


class Config(db.Document):
    data = db.DictField(required=True)
    creator = db.ReferenceField("User", required=True, unique=True)
    meta = {"collection": "configuration"}
