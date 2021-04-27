from flask import Blueprint
from nomenclate_api.models.user import User
from nomenclate_api.utils.responses import format_response

user_routes = Blueprint("user_routes", __name__)

base = "/users"


@user_routes.route(base, methods=["GET"])
def list():
    print(User.find())
    return format_response({"success": True}, 200)


@user_routes.route("/login", methods=["POST"])
def login():
    try:
        # id = request.json["id"]
        # todo_ref.document(id).set(request.json)
        return format_response({"success": True}, 200)
    except Exception as e:
        return format_response(
            {"success": False, "message": f"An Error Occured: {e}"}, 500
        )
