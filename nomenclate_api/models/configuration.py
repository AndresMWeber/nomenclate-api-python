from flask import request
from flask_jwt_extended import get_jwt_identity
from nomenclate_api.db.config import db


class Config(db.Document):
    name = db.StringField(default="default", required=True, unique_with=["creator"])
    data = db.DictField(required=True)
    creator = db.ReferenceField("User", required=True)
    meta = {"collection": "configuration"}

    @classmethod
    def from_request(cls, name=None):
        return Config.objects.get(name=name or request.json.get("name"), creator=get_jwt_identity())
