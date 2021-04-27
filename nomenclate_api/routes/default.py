from flask import request, jsonify, Blueprint

default_routes = Blueprint("default_routes", __name__)


@default_routes.route("/")
def hello():
    print('default')
    return "Hello World!"


@default_routes.route("/add", methods=["POST"])
def create():
    """
    create() : Add document to Firestore collection with request body
    Ensure you pass a custom ID as part of json body in post request
    e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        id = request.json["id"]
        # todo_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@default_routes.route("/list", methods=["GET"])
def read():
    """
    read() : Fetches documents from Firestore collection as JSON
    todo : Return document that matches query ID
    all_todos : Return all documents
    """
    try:
        # Check if ID was passed to URL query
        todo_id = request.args.get("id")
        if todo_id:
            # todo = todo_ref.document(todo_id).get()
            return jsonify({"success": True}), 200
        else:
            # all_todos = [doc.to_dict() for doc in todo_ref.stream()]
            return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@default_routes.route("/update", methods=["POST", "PUT"])
def update():
    """
    update() : Update document in Firestore collection with request body
    Ensure you pass a custom ID as part of json body in post request
    e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json["id"]
        # todo_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@default_routes.route("/delete", methods=["GET", "DELETE"])
def delete():
    """
    delete() : Delete a document from Firestore collection
    """
    try:
        # Check for ID in URL query
        todo_id = request.args.get("id")
        # todo_ref.document(todo_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
