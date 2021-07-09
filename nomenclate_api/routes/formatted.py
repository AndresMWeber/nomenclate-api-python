from copy import deepcopy
from pprint import pprint
from operator import itemgetter
from flask_jwt_extended import jwt_required
from nomenclate import Nom
from nomenclate_api.db.mongo import LOG
from nomenclate_api.models.nomenclate import Nomenclate
from nomenclate_api.utils.responses import format_response, format_error
from .base import ApiRoute


class FormattedApi(ApiRoute):
    @jwt_required()
    def get(self, id):
        """Retrieve formatted string from a Nomenclate object by id
        ---
        schema:
            security:
                - JWTAuth: []
            responses:
                200:
                    description: Return a formatted nomenclate string
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
            nomenclate = Nomenclate.from_request(id)
            format_data, format_string = itemgetter("data", "format_string")(nomenclate)
            instance = Nom(format_data, format_string)
            config = nomenclate.config.to_mongo().to_dict()
            instance.set_config(config["data"])
            return format_response({"data": instance.get()})
        except Exception as e:
            LOG.error(e)
            return format_error("The requested nomenclate does not exist.", 404)
