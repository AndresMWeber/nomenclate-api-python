from .config import db


class Config(db.Document):
    meta = {"collection": "configuration"}
    data = db.DictField(required=True)
