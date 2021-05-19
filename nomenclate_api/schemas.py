from nomenclate_api.utils.general import classproperty
from marshmallow import Schema, fields


class BaseSchema(Schema):
    @classproperty
    def simple_name(cls: Schema) -> str:
        return cls.__name__.replace("Schema", "")


class LoginResponseSchema(BaseSchema):
    token = fields.String(required=True)


class ErrorSimpleSchema(BaseSchema):
    error = fields.String(required=True)


class ErrorComplexSchema(BaseSchema):
    error = fields.Dict(required=True)


class ConfigurationPostSchema(BaseSchema):
    data = fields.Dict(required=True)
    name = fields.String(required=True)


class ConfigurationPutSchema(ConfigurationPostSchema):
    _id = fields.String(required=True)


class EmailSchema(BaseSchema):
    email = fields.String(required=True)


class EmailPasswordSchema(EmailSchema):
    password = fields.String(required=True)


class NameEmailPasswordSchema(EmailPasswordSchema):
    name = fields.String(required=True)
