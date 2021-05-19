from os import getenv
from typing import Tuple, List
from dotenv import load_dotenv
from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_restful import Api
from .utils.responses import JSONEncoder
from .models.user import login_manager
from .api_spec import create_spec
from .routes.base import ApiRoute
from .routes.auth import SignupApi, LoginApi, DeactivateApi, ReactivateApi, UserExistsApi
from .routes.profile import ActiveConfigApi, ProfileConfigApi, ProfileApi
from .routes.configuration import ConfigApi, ConfigGetApi
from .routes.nomenclate import NomenclateApi

routes: Tuple[ApiRoute, str] = [
    (SignupApi, "/auth/signup"),
    (LoginApi, "/auth/login"),
    (UserExistsApi, "/auth/exists"),
    (DeactivateApi, "/auth/deactivate"),
    (ReactivateApi, "/auth/reactivate"),
    (ProfileApi, "/me"),
    (ProfileConfigApi, "/me/configs"),
    (ActiveConfigApi, "/me/config"),
    (ConfigApi, "/config"),
    (ConfigGetApi, "/config/<string:name>"),
    (NomenclateApi, "/nomenclate"),
]


def create_app():
    load_dotenv()
    app = Flask(__name__.replace(".api", "").replace("_", " ").title())
    Bcrypt(app)
    JWTManager(app)
    api = Api(app)

    mongo_uri = getenv("MONGO_URI")
    if not mongo_uri or mongo_uri == "undefined":
        mongo_uri = "mongodb://localhost:27017/nomenclate-api"
    app.config["MONGODB_SETTINGS"] = {"host": mongo_uri}
    app.config["JWT_SECRET_KEY"] = getenv("SECRET") or "insecure"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
    app.json_encoder = JSONEncoder

    from nomenclate_api.db.config import db

    db.init_app(app)
    login_manager.init_app(app)

    [api.add_resource(route, path) for route, path in routes]

    with app.app_context():
        print(f"Connecting to DB: {mongo_uri}")
        print(f"Connection state: {db.connection}")

    return app


port = int(getenv("PORT") or 8080)
app = create_app()
spec = create_spec(app, routes)

if __name__ == "__main__":
    app.run(threaded=True, host="0.0.0.0", port=port)
