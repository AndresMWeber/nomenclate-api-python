from flask import Response, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from nomenclate_api.models.nomenclate import Nomenclate


class NomenclateApi(Resource):
    @jwt_required()
    def post(self):
        body = request.get_json()
        instance = Nomenclate(**body).save()

    @jwt_required()
    def put(self, id):
        body = request.get_json()
        Nomenclate.objects.get(id=id).update(**body)
        return "", 200

    @jwt_required()
    def delete(self, id):
        instance = Nomenclate.objects.get(id=id).delete()
        return "", 200
