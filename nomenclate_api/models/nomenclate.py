from .config import db


class Nomenclate(db.Document):
    meta = {"collection": "nomenclate"}
    data = db.DictField(required=True)
