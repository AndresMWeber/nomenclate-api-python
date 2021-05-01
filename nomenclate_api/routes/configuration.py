from logging import getLogger
from mongoengine.errors import NotUniqueError
from pymongo.errors import DuplicateKeyError
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from nomenclate_api.db.config import db
from ..models.configuration import Config
from ..models.user import User
from ..utils.responses import format_response, format_error


log = getLogger()


class ConfigApi(Resource):
    decorators = [jwt_required()]

    def get(self, name):
        try:
            return format_response(Config.from_request(name).to_mongo())
        except:
            return format_error("The requested configuration does not exist.", 404)

    def post(self):
        try:
            Config(creator=User.get_from_jwt(), **request.get_json()).save()
            return format_response()
        except (NotUniqueError, DuplicateKeyError):
            return format_error("The specified configuration already exists.", 409)

    def put(self):
        try:
            request_json = request.get_json()
            request_json.pop("creator")
            id = request_json.pop("_id")
            Config.objects.get(id=id).update(**request.get_json())
            return format_response()
        except Exception as e:
            print(e)
            return format_error("The requested resource does not exist.", 404)

    def delete(self, name):
        try:
            Config.from_request(name).delete()
            return format_response()
        except:
            return format_error("The requested configuration does not exist.", 404)
