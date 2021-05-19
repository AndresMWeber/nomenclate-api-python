import json
from toml import load as toml_load
from marshmallow import Schema, fields
from apispec import APISpec
from apispec.exceptions import APISpecError
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import current_app
from nomenclate_api.utils.general import classproperty
from flask import current_app
from flask.views import MethodView
from apispec import yaml_utils
from apispec.exceptions import APISpecError


class FlaskRestfulPlugin(FlaskPlugin):
    @staticmethod
    def _rule_for_view(view, app):
        if app is None:
            app = current_app

        view_funcs = app.view_functions
        endpoint = None
        for ept, view_func in view_funcs.items():
            if view_func.__name__ == view.__name__:
                endpoint = ept
        if not endpoint:
            raise APISpecError(f"Could not find endpoint for view {view}")

        return app.url_map._rules_by_endpoint[endpoint][0]


class BaseSchema(Schema):
    @classproperty
    def simple_name(cls: Schema) -> str:
        return cls.__name__.replace("Schema", "")


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


def create_spec(current_app, routes) -> APISpec:
    pyproject_data = toml_load("pyproject.toml")["tool"]["poetry"]
    version = pyproject_data["version"]
    spec = APISpec(
        title=current_app.name,
        version=version,
        openapi_version="3.0.2",
        info=dict(
            description=current_app.name,
            version=version,
            contact=dict(email=pyproject_data["authors"]),
            license=dict(name="Apache 2.0", url="http://www.apache.org/licenses/LICENSE-2.0.html"),
        ),
        servers=[dict(description="Production Server", url=pyproject_data["urls"]["server"])],
        tags=pyproject_data["keywords"],
        plugins=[FlaskRestfulPlugin(), MarshmallowPlugin()],
    )

    def register_schema(schema: Schema):
        spec.components.schema(schema.simple_name, schema=schema)

    register_schema(ErrorSimpleSchema)
    register_schema(ErrorComplexSchema)
    register_schema(ConfigurationPostSchema)
    register_schema(ConfigurationPutSchema)
    register_schema(EmailSchema)
    register_schema(EmailPasswordSchema)
    register_schema(NameEmailPasswordSchema)

    with current_app.test_request_context():
        for route, _ in routes:
            spec.path(view=route.as_view(route.name))

    with open(f"docs/spec/json/nomenclate_{version}.json", "w") as f:
        json.dump(spec.to_dict(), f, sort_keys=True, indent=4)

    with open(f"docs/spec/yaml/nomenclate_{version}.yaml", "w") as f:
        f.write(spec.to_yaml())
    return spec
