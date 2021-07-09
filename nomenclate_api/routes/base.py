import functools
from typing import Dict, List
from marshmallow import ValidationError
from flask_restful import Resource
from bson.objectid import ObjectId
from flask import request
from mongoengine.base.fields import ObjectIdField
from nomenclate_api.config import LOG
from nomenclate_api.utils.responses import format_error
from nomenclate_api.utils.general import classproperty


class ApiRoute(Resource):
    @classproperty
    def name(cls) -> str:
        return cls.__name__.lower()

    @staticmethod
    def convert_object_ids(object_id_fields: List[str], body: Dict) -> Dict:
        for field in object_id_fields:
            body[field] = ObjectId(body[field])
        return body

    @staticmethod
    def strip_body_id(body: Dict) -> str:
        id = body.get("_id")
        body.pop("_id")
        return id

    def log_error(self, msg: str):
        LOG.error(msg)

    def log_warning(self, msg: str):
        LOG.warning(msg)

    def log(self, msg: str):
        LOG.info(msg)


def validate_schema(schema):
    def decorator(func):
        @functools.wraps(func)
        def method_wrapper(self, *args, **kwargs):
            try:
                payload = request.get_json()
                schema.load(payload)
            except ValidationError as e:
                return format_error(e.normalized_messages(), 400)

            return func(self, *args, **kwargs)

        return method_wrapper

    return decorator
