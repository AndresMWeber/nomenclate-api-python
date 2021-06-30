from flask import request
from flask_jwt_extended import get_jwt_identity
from nomenclate_api.db.mongo import db


class Nomenclate(db.Document):
    name = db.StringField(required=True)
    data = db.DictField(required=True)
    config = db.ReferenceField("Config", required=True)
    creator = db.ReferenceField("User", required=True)
    format_string = db.StringField()
    org = db.ReferenceField("Organization")
    meta = {"collection": "nomenclate"}

    @classmethod
    def from_request(cls, id=None):
        return Nomenclate.objects.get(id=id or request.json.get("_id"), creator=get_jwt_identity())
