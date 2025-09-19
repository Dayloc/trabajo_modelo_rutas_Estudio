from flask import Flask, request, jsonify, url_for, Blueprint
from utils import generate_sitemap, APIException
from models import db, User, Tarea
from flask_cors import CORS




api = Blueprint("api", __name__, url_prefix="/api")

CORS(api)

# -------------------- USERS --------------------
@api.route("/users", methods=["POST"])
def create_user():
    data = request.json
    user = User.create(email=data["email"])
    return jsonify(user.serialize()), 201

@api.route("/users", methods=["GET"])
def get_users():
    users = User.get_all()
    return jsonify([u.serialize() for u in users]), 200

@api.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.get_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.serialize()), 200

@api.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    user = User.update_email(user_id, data.get("email"))
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.serialize()), 200

@api.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    success = User.delete(user_id)
    if not success:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": f"User {user_id} deleted"}), 200

# -------------------- TAREAS --------------------
@api.route("/tareas", methods=["POST"])
def create_tarea():
    data = request.json
    tarea = Tarea.create(title=data["title"], user_id=data["user_id"], completed=data.get("completed", False))
    return jsonify(tarea.serialize()), 201

@api.route("/tareas", methods=["GET"])
def get_tareas():
    tareas = Tarea.get_all()
    return jsonify([t.serialize() for t in tareas]), 200

@api.route("/tareas/<int:tarea_id>", methods=["GET"])
def get_tarea(tarea_id):
    tarea = Tarea.get_by_id(tarea_id)
    if not tarea:
        return jsonify({"error": "Tarea not found"}), 404
    return jsonify(tarea.serialize()), 200

@api.route("/tareas/<int:tarea_id>", methods=["PUT"])
def update_tarea(tarea_id):
    data = request.json
    tarea = Tarea.update(
        tarea_id,
        title=data.get("title"),
        completed=data.get("completed")
    )
    if not tarea:
        return jsonify({"error": "Tarea not found"}), 404
    return jsonify(tarea.serialize()), 200

@api.route("/tareas/<int:tarea_id>", methods=["DELETE"])
def delete_tarea(tarea_id):
    success = Tarea.delete(tarea_id)
    if not success:
        return jsonify({"error": "Tarea not found"}), 404
    return jsonify({"message": f"Tarea {tarea_id} deleted"}), 200
