from flask import Response, request
from flask_jwt_extended import jwt_required
from nomenclate_api.models.configuration import Config
from flask_restful import Resource


class ConfigApi(Resource):
    @jwt_required
    def post(self):
        body = request.get_json()
        movie = Config(**body).save()
        return "", 200

    @jwt_required
    def put(self, id):
        body = request.get_json()
        Config.objects.get(id=id).update(**body)
        return "", 200

    @jwt_required
    def delete(self, id):
        movie = Config.objects.get(id=id).delete()
        return "", 200
