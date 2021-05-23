from nomenclate_api.utils.general import classproperty
from marshmallow import Schema, fields


class BaseSchema(Schema):
    @classproperty
    def simple_name(cls: Schema) -> str:
        return cls.__name__.replace("Schema", "")


class ConfigResponseSchema(BaseSchema):
    name = fields.String(required=True)
    data = fields.String(required=True)
    creator = fields.Dict(required=True)
    meta = fields.Dict(required=True)


class LoginResponseSchema(BaseSchema):
    token = fields.String(required=True)


class SignupResponseSchema(BaseSchema):
    id = fields.String(required=True)


class ErrorSimpleSchema(BaseSchema):
    error = fields.String(required=True)


class ErrorComplexSchema(BaseSchema):
    error = fields.Dict(required=True)


class ConfigurationPostSchema(BaseSchema):
    data = fields.Dict(required=True)
    name = fields.String(required=True)


class ConfigurationPutSchema(ConfigurationPostSchema):
    _id = fields.String(required=True)
    creator = fields.String()


class EmailSchema(BaseSchema):
    email = fields.String(required=True)


class EmailPasswordSchema(EmailSchema):
    password = fields.String(required=True)


class NameEmailPasswordSchema(EmailPasswordSchema):
    name = fields.String(required=True)


class ExistsResponseSchema(EmailPasswordSchema):
    exists = fields.Boolean(required=True)


SCHEMAS = [
    BaseSchema,
    LoginResponseSchema,
    SignupResponseSchema,
    ErrorSimpleSchema,
    ErrorComplexSchema,
    ConfigurationPostSchema,
    ConfigurationPutSchema,
    EmailSchema,
    EmailPasswordSchema,
    NameEmailPasswordSchema,
    ExistsResponseSchema,
]
