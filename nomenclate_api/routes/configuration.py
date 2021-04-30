from mongoengine.errors import NotUniqueError
from pymongo.errors import DuplicateKeyError
from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from ..models.configuration import Config
from ..models.user import User
from ..utils.responses import format_response, format_error


class ConfigApi(Resource):
    @jwt_required()
    def get(self):
        try:
            return format_response(Config.objects.get(creator=get_jwt_identity()))
        except:
            return format_error("You do not have a configuration.", 404)

    @jwt_required()
    def post(self):
        json = request.get_json()
        try:
            Config(creator=User.get_from_jwt(), **request.get_json()).save()
            return format_response()
        except (NotUniqueError, DuplicateKeyError):
            return format_error("You already have a configuration set up.", 409)

    @jwt_required()
    def put(self):
        body = request.get_json()
        try:
            Config.objects.get(creator=get_jwt_identity()).update(**body)
            return format_response()
        except:
            return format_error("You do not have a configuration.", 404)

    @jwt_required()
    def delete(self):
        try:
            Config.objects.get(creator=get_jwt_identity()).delete()
            return format_response()
        except:
            return format_error("You do not have a configuration.", 404)
