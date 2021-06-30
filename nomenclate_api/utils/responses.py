from typing import List, Tuple, Union
from flask import jsonify, make_response
from bson.objectid import ObjectId
import datetime
import json


def format_response(payload: dict = None, status: int = 200) -> Tuple[str, int]:
    if payload == None and status >= 200 and status <= 299:
        payload = {"success": True}
    if isinstance(payload, str):
        payload = {"message": payload}
    return make_response(jsonify(payload), status)


def format_error(message: Union[str, List[str]], status: int = 400) -> Tuple[str, int]:
    return format_response({"error": message}, status)


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
