import functools
from marshmallow import ValidationError
from flask_restful import Resource
from flask import request
from nomenclate_api.config import LOG
from nomenclate_api.utils.responses import format_error
from nomenclate_api.utils.general import classproperty


class ApiRoute(Resource):
    @classproperty
    def name(cls) -> str:
        return cls.__name__.lower()

    def log_error(self, msg):
        LOG.error(msg)

    def log_warning(self, msg):
        LOG.warning(msg)

    def log(self, msg):
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
