from os import environ
from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from .utils.responses import JSONEncoder
from .models.user import login_manager
from flask_restful import Api


def create_app():
    load_dotenv()
    app = Flask(__name__)
    api = Api(app)

    app.config["MONGODB_SETTINGS"] = {
        "DB": "dev",
        "host": environ.get("MONGO_URI", "mongodb://localhost:27017/"),
    }
    app.config["JWT_SECRET_KEY"] = environ.get("SECRET")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
    app.json_encoder = JSONEncoder

    from .models.config import db

    db.init_app(app)
    login_manager.init_app(app)

    from .routes.default import default_routes
    from .routes.user import user_routes

    app.register_blueprint(default_routes)
    app.register_blueprint(user_routes)

    from .auth import SignupApi, LoginApi
    from .routes.configuration import ConfigApi
    from .routes.nomenclate import NomenclateApi

    api.add_resource(SignupApi, "/auth/signup")
    api.add_resource(LoginApi, "/auth/login")
    api.add_resource(NomenclateApi, "/nom")
    api.add_resource(ConfigApi, "/cfg")

    Bcrypt(app)
    JWTManager(app)

    return app


port = int(environ.get("PORT", 8080))
app = create_app()

if __name__ == "__main__":
    app.run(threaded=True, host="0.0.0.0", port=port)
