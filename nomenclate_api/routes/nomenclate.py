from flask import request
from flask_jwt_extended import jwt_required
from nomenclate_api.models.nomenclate import Nomenclate
from nomenclate_api.utils.responses import format_response, format_error
from .base import ApiRoute


class NomenclateApi(ApiRoute):
    @jwt_required()
    def post(self):
        """Create Nomenclate from Active Config + Payload
        ---
        schema:
            security:
                - JWTAuth: []
            responses:
                201:
                    description: Return a nomenclate object
                    content:
                        application/json:
                            schema: Base
                400:
                    description: The supplied payload is invalid.
                    content:
                        application/json:
                            schema: ErrorSimple
        """
        try:
            body = request.get_json()
            instance = Nomenclate(**body).save()
            return format_response({"nomenclate": instance}, 201)
        except:
            return format_error("The supplied payload is invalid.", 400)

    @jwt_required()
    def put(self, id):
        """Update Nomenclate from Active Config + Payload
        ---
        schema:
            security:
                - JWTAuth: []
            responses:
                204:
                    description: Sucessfully updated the nomenclate object
                400:
                    description: The supplied payload is invalid.
                    content:
                        application/json:
                            schema: ErrorSimple
        """
        try:
            body = request.get_json()
            Nomenclate.objects.get(id=id).update(**body)
            return format_response()
        except:
            return format_error("The supplied payload is invalid.", 400)

    @jwt_required()
    def delete(self, id):
        """Update Nomenclate from Active Config + Payload
        ---
        schema:
            security:
                - JWTAuth: []
            responses:
                204:
                    description: Sucessfully deleted the nomenclate object
                404:
                    description: The nomenclate object is invalid.
                    content:
                        application/json:
                            schema: ErrorSimple
        """
        try:
            Nomenclate.objects.get(id=id).delete()
            return format_response()
        except:
            return format_error("The requested configuration does not exist.", 404)
