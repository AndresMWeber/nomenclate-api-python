from os import getenv, environ
from dotenv import load_dotenv
from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_restful import Api
from .utils.responses import JSONEncoder
from .models.user import login_manager


def create_app():
    load_dotenv()
    app = Flask(__name__)
    api = Api(app)
    mongo_uri = getenv("MONGO_URI")
    if not mongo_uri or mongo_uri == "undefined":
        mongo_uri = "mongodb://localhost:27017/nomenclate-api"
    app.config["MONGODB_SETTINGS"] = {"host": mongo_uri}
    app.config["JWT_SECRET_KEY"] = getenv("SECRET") or "insecure"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
    app.json_encoder = JSONEncoder

    from .models.config import db

    db.init_app(app)

    login_manager.init_app(app)

    from .routes.default import default_routes

    app.register_blueprint(default_routes)

    from .routes.auth import SignupApi, LoginApi, DeactivateApi, ReactivateApi
    from .routes.configuration import ConfigApi
    from .routes.nomenclate import NomenclateApi

    api.add_resource(SignupApi, "/auth/signup")
    api.add_resource(LoginApi, "/auth/login")
    api.add_resource(DeactivateApi, "/auth/deactivate")
    api.add_resource(ReactivateApi, "/auth/reactivate")
    api.add_resource(NomenclateApi, "/nomenclate")
    api.add_resource(ConfigApi, "/config")

    Bcrypt(app)
    JWTManager(app)

    with app.app_context():
        print(f"Connecting to DB: {mongo_uri}")
        print(f"Connection state: {db.connection}")

    return app


port = int(getenv("PORT") or 8080)
app = create_app()

if __name__ == "__main__":
    app.run(threaded=True, host="0.0.0.0", port=port)
