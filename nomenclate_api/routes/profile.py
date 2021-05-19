from logging import getLogger
from flask import request
from flask_jwt_extended import jwt_required
from nomenclate_api.models.configuration import Config
from nomenclate_api.models.user import User
from nomenclate_api.utils.responses import format_response, format_error
from .base import ApiRoute

log = getLogger()


class ProfileApi(ApiRoute):
    decorators = [jwt_required()]

    def get(self):
        """User Profile
        ---
        schema:
            responses:
                200:
                    description: Return a Profile
                    content:
                        application/json:
                            schema: Base
                404:
                    description: The user from the current credentials does not exist
                    content:
                        application/json:
                            schema: ErrorSimple
        """
        try:
            user = User.get_from_jwt().to_mongo().to_dict()
            user.pop("password")
            return format_response(user)
        except Exception as e:
            log.error(e)
            return format_error("You do not exist. Contemplate.", 404)


class ProfileConfigApi(ApiRoute):
    decorators = [jwt_required()]

    def get(self):
        """User's Configs
        ---
        schema:
            responses:
                200:
                    description: Return all configs created by the logged in user
                    content:
                        application/json:
                            schema: Base
                404:
                    description: Missing config
                    content:
                        application/json:
                            schema: ErrorSimple
        """
        try:
            return format_response(
                {"configurations": Config.objects.filter(creator=User.get_from_jwt())}
            )
        except Exception as e:
            log.error(e)
            return format_error("The requested configuration does not exist.", 404)


class ActiveConfigApi(ApiRoute):
    decorators = [jwt_required()]

    def get(self):
        """User's Active Config
        ---
        schema:
            responses:
                200:
                    description: Return the logged in user's active config
                    content:
                        application/json:
                            schema: Base
                404:
                    description: Missing config
                    content:
                        application/json:
                            schema: ErrorSimple
        """
        try:
            return format_response({"configuration": User.get_from_jwt().config})
        except Exception as e:
            log.error(e)
            return format_error("The requested configuration does not exist.", 404)

    def post(self):
        """Set the named config to be the logged in user's active config
        ---
        schema:
            responses:
                200:
                    description: Return a Profile
                    content:
                        application/json:
                            schema: Base
                404:
                    description: Missing config
                    content:
                        application/json:
                            schema: ErrorSimple
        """
        try:
            user = User.get_from_jwt()
            user.config = Config.objects.get(
                creator=User.get_from_jwt(), name=request.json.get("name")
            )
            user.save()
            return format_response()
        except Exception as e:
            log.error(e)
            return format_error("The requested configuration does not exist.", 404)
