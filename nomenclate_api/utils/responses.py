from typing import Tuple
from flask import jsonify
from bson.objectid import ObjectId
import datetime
import json

def format_response(payload: dict, status: int) -> Tuple[str, int]:
    return jsonify(payload), status


class JSONEncoder(json.JSONEncoder):
    """extend json-encoder class"""

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, set):
            return list(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)
