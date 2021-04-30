from .config import db


class Nomenclate(db.Document):
    data = db.DictField(required=True)
    creator = db.ReferenceField("User", required=True)
    formatted = db.StringField()
    org = db.ReferenceField("Organization")
    meta = {"collection": "nomenclate"}
