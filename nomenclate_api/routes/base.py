import functools
from marshmallow import Schema, ValidationError
from flask_restful import Resource
from flask import request
from ..utils.responses import format_error


class BaseSchema(Schema):
    pass


class ApiRoute(Resource):
    pass


def validate_schema(schema):
    def decorator(func):
        @functools.wraps(func)
        def method_wrapper(self, *args, **kwargs):
            try:
                payload = request.get_json()
                schema.load(payload)
            except ValidationError as err:
                return format_error(err.messages, 400)

            return func(self, *args, **kwargs)

        return method_wrapper

    return decorator
