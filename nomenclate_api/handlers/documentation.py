import json


def handler(event, context):
    response = {}
    response["statusCode"] = 302
    response["headers"] = {"Location": "https://nomenclate.readme.io/"}
    data = {}
    response["body"] = json.dumps(data)
    return response
