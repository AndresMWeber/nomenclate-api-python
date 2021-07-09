from nomenclate_api.db.mongo import LOG
from mongoengine.errors import NotUniqueError
from pymongo.errors import DuplicateKeyError
from pprint import pprint
from flask import request
from flask_jwt_extended import jwt_required
from nomenclate_api.models.nomenclate import Nomenclate
from nomenclate_api.models.user import User
from nomenclate_api.schemas import NomenclatePostSchema, NomenclatePutSchema
from nomenclate_api.utils.responses import format_response, format_error
from .base import ApiRoute, validate_schema


class NomenclateApi(ApiRoute):
    @jwt_required()
    @validate_schema(NomenclatePostSchema())
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
                            schema: NomenclateResponseSchema
                400:
                    description: The supplied payload is invalid.
                    content:
                        application/json:
                            schema: ErrorSimple
                400:
                    description: Missing active config and/or config not supplied.
                    content:
                        application/json:
                            schema: ErrorSimple
        """
        try:
            body = request.get_json()
            user = User.get_from_jwt()
            body["creator"] = user
            try:
                body["config"] = user.config
            except Exception as e:
                return format_error("There was a problem retrieving your active config.")
            nomenclate = Nomenclate(**body).save()
            return format_response({"nomenclate": nomenclate.to_mongo().to_dict()}, 201)
        except (NotUniqueError, DuplicateKeyError) as e:
            LOG.error(e)
            return format_error("The supplied payload is invalid.", 400)

    @jwt_required()
    @validate_schema(NomenclatePutSchema())
    def put(self):
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
            body = self.convert_object_ids(["config", "creator"], request.get_json())
            id = self.strip_body_id(body)
            Nomenclate.from_request(id).update(**body)
            return format_response(None, 204)
        except Exception as e:
            LOG.error(e)
            return format_error("The supplied payload is invalid.", 400)


class NomenclateApiById(ApiRoute):
    @jwt_required()
    def get(self, id):
        """Retrieve Nomenclate object by id
        ---
        schema:
            security:
                - JWTAuth: []
            responses:
                200:
                    description: Return a nomenclate objet
                    content:
                        application/json:
                            schema: NomenclateResponseSchema
                404:
                    description: Could not find nomenclate object
                    content:
                        application/json:
                            schema: ErrorSimple
        """
        try:
            return format_response(Nomenclate.from_request(id).to_mongo().to_dict())
        except Exception as e:
            LOG.error(e)
            return format_error("The requested nomenclate does not exist.", 404)

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
            Nomenclate.from_request(id).delete()
            return format_response()
        except:
            return format_error("The requested configuration does not exist.", 404)
