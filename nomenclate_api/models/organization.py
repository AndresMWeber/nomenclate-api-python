from nomenclate_api.db.config import db


class Organization(db.Document):
    title = db.StringField(required=True)
    owner = db.ReferenceField("User")
    meta = {"collection": "organization"}
