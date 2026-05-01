from flask import Blueprint, request, jsonify, session
from backend.auth.auth_service import register_user, login_user

auth_bp = Blueprint("auth", __name__)


# -------------------
# REGISTER
# -------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify({
            "success": False,
            "message": "Username required"
        }), 400

    result = register_user(username)
    return jsonify(result)


# -------------------
# LOGIN
# -------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")

    result = login_user(username)

    if result["success"]:
        session["user"] = username

    return jsonify(result)


# -------------------
# CURRENT USER CHECK (VERY IMPORTANT FOR FRONTEND)
# -------------------
@auth_bp.route("/me", methods=["GET"])
def me():
    user = session.get("user")

    if not user:
        return jsonify({"logged_in": False})

    return jsonify({
        "logged_in": True,
        "user": user
    })


# -------------------
# LOGOUT
# -------------------
@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()

    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    })