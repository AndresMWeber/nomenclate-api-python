from os import getenv
from typing import Tuple
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_restful import Api
from .config import ACCESS_EXPIRES
from .utils.responses import JSONEncoder
from .models.user import login_manager
from .routes.base import ApiRoute
from .routes.auth import (
    SignupApi,
    LoginApi,
    LogoutApi,
    DeactivateApi,
    ReactivateApi,
    UserExistsApi,
)
from .routes.profile import ActiveConfigApi, ProfileConfigApi, ProfileApi
from .routes.configuration import ConfigApi, ConfigByNameApi
from .routes.nomenclate import NomenclateApi
from .db.mongo import init_mongo
from .db.blacklist import init_blacklist


ROUTES: Tuple[ApiRoute, str] = [
    (SignupApi, "/auth/signup"),
    (LoginApi, "/auth/login"),
    (LogoutApi, "/auth/logout"),
    (UserExistsApi, "/auth/exists"),
    (DeactivateApi, "/auth/deactivate"),
    (ReactivateApi, "/auth/reactivate"),
    (ProfileApi, "/me"),
    (ProfileConfigApi, "/me/configs"),
    (ActiveConfigApi, "/me/config"),
    (ConfigApi, "/config"),
    (ConfigByNameApi, "/config/<string:name>"),
    (NomenclateApi, "/nomenclate"),
]


def create_app():
    load_dotenv()

    app = Flask(__name__.replace(".api", "").replace("_", " ").title())
    Bcrypt(app)
    api = Api(app)
    jwt = JWTManager(app)

    app.json_encoder = JSONEncoder
    app.config["JWT_SECRET_KEY"] = getenv("SECRET") or "insecure"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES

    init_mongo(app)
    init_blacklist(app, jwt)
    login_manager.init_app(app)

    [api.add_resource(route, path) for route, path in ROUTES]

    return app


port = int(getenv("PORT") or 8080)
app = create_app()

if __name__ == "__main__":
    app.run(threaded=True, host="0.0.0.0", port=port)
