from .config import db


class Organization(db.Document):
    title = db.StringField(required=True)
    owner = ReferenceField("User")
    meta = {"collection": "organization"}
