from nomenclate_api.db.config import db
from flask_jwt_extended import get_jwt_identity


def is_owner(document: db.Document):
    return document.creator == get_jwt_identity()


def is_member(document: db.Document):
    return document.to_mongo().values() == get_jwt_identity()
