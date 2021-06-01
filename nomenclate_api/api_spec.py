import re
import json
from marshmallow import Schema
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from nomenclate_api.utils.general import get_project_attribute
from nomenclate_api.openapi_plugin import FlaskRestfulPlugin
from nomenclate_api.schemas import SCHEMAS


def create_spec(current_app, routes) -> APISpec:
    project_data = get_project_attribute("tool", "poetry")
    version = project_data["version"]

    spec = APISpec(
        title=current_app.name,
        version=version,
        openapi_version="3.0.2",
        info=dict(
            description=current_app.name,
            version=version,
            contact=dict(email=re.search("<(.*)>", project_data["authors"][0])[1]),
            license=dict(name="Apache 2.0", url="http://www.apache.org/licenses/LICENSE-2.0.html"),
        ),
        servers=[dict(description="Production Server", url=project_data["urls"]["server"])],
        tags=[],
        plugins=[FlaskRestfulPlugin(), MarshmallowPlugin()],
    )

    jwt_scheme = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    spec.components.security_scheme("JWTAuth", jwt_scheme)

    def register_schema(schema: Schema):
        spec.components.schema(schema.simple_name, schema=schema)

    [register_schema(schema) for schema in SCHEMAS]

    with current_app.test_request_context():
        for route, _ in routes:
            spec.path(view=route.as_view(route.name))

    write_doc_files(spec, version)
    return spec


def write_doc_files(spec, version):

    with open(f"docs/spec/json/nomenclate_{version}.json", "w") as f:
        json.dump(spec.to_dict(), f, sort_keys=True, indent=4)

    with open(f"docs/spec/yaml/nomenclate_{version}.yaml", "w") as f:
        f.write(spec.to_yaml())

    with open(f"docs/spec/json/nomenclate.json", "w") as f:
        json.dump(spec.to_dict(), f, sort_keys=True, indent=4)

    with open(f"docs/spec/yaml/nomenclate.yaml", "w") as f:
        f.write(spec.to_yaml())


def run():
    from nomenclate_api.api import create_app, ROUTES

    create_spec(create_app(), ROUTES)


if __name__ == "__main__":
    run()
