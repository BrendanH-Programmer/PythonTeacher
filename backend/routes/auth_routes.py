from flask import Blueprint, request, jsonify, session

# ✅ FIXED IMPORT
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
# LOGOUT
# -------------------
@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)

    return jsonify({
        "success": True,
        "message": "Logged out"
    })