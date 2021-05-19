from nomenclate_api.utils.general import get_project_attribute


def handler(event, context):
    response = {
        "statusCode": 200,
        "body": f"Welcome to Nomenclate API version {get_project_attribute('tool','poetry','version')}!",
    }
    return response
