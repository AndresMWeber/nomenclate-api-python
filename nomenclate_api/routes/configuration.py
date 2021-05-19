from logging import getLogger
from mongoengine.errors import NotUniqueError
from pymongo.errors import DuplicateKeyError
from flask import request
from flask_jwt_extended import jwt_required
from nomenclate_api.models.user import User
from nomenclate_api.models.configuration import Config
from nomenclate_api.utils.responses import format_response, format_error
from nomenclate_api.api_spec import ConfigurationPostSchema, ConfigurationPutSchema
from .base import ApiRoute, validate_schema

log = getLogger()


class ConfigApi(ApiRoute):
    decorators = [jwt_required()]

    @validate_schema(ConfigurationPostSchema())
    def post(self):
        try:
            config = Config(creator=User.get_from_jwt(), **request.get_json()).save()
            return format_response(config, 201)
        except (NotUniqueError, DuplicateKeyError):
            return format_error("The specified configuration already exists.", 409)

    @validate_schema(ConfigurationPutSchema())
    def put(self):
        try:
            request_json = request.get_json()
            config = Config.objects.get(id=request_json.get("_id")).update(**request_json)
            return format_response(config, 204)
        except Exception as e:
            log.error(e)
            return format_error("The requested resource does not exist.", 404)

    def delete(self, name: str):
        try:
            Config.from_request(name).delete()
            return format_response()
        except Exception as e:
            log.error(e)
            return format_error("The requested configuration does not exist.", 404)


class ConfigGetApi(ApiRoute):
    decorators = [jwt_required()]

    def get(self, name: str):
        try:
            return format_response(Config.from_request(name).to_mongo().to_dict())
        except:
            return format_error("The requested configuration does not exist.", 404)
