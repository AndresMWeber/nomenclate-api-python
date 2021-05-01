from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from ..models.configuration import Config
from ..models.user import User
from ..utils.responses import format_response, format_error


class ProfileApi(Resource):
    decorators = [jwt_required()]

    def get(self):
        try:
            user = User.get_from_jwt().to_mongo()
            user.pop("password")
            configuration = user["config"]
            user["config"] = Config.objects.get(id=configuration)["name"] if configuration else None
            return format_response(user)
        except Exception as e:
            print(e)
            return format_error("You do not exist. Contemplate.", 404)


class ProfileConfigApi(Resource):
    decorators = [jwt_required()]

    def get(self):
        try:
            return format_response(
                {"configurations": Config.objects.filter(creator=User.get_from_jwt())}
            )
        except Exception as e:
            print(e)
            return format_error("The requested configuration does not exist.", 404)


class ActiveConfigApi(Resource):
    decorators = [jwt_required()]

    def get(self):
        try:
            return format_response({"configuration": User.get_from_jwt().config})
        except:
            return format_error("The requested configuration does not exist.", 404)

    def post(self):
        try:
            user = User.get_from_jwt()
            user.config = Config.objects.get(
                creator=User.get_from_jwt(), name=request.json.get("name")
            )
            user.save()
            return format_response()
        except Exception as e:
            print(e)
            return format_error("The requested configuration does not exist.", 404)
