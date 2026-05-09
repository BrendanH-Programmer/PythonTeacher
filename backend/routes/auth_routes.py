# -------------------------
# AUTH ROUTES 
# Handles user registration, login, logout, and session management
# -------------------------

from flask import Blueprint, request, jsonify, session
from backend.auth.auth_service import register_user, login_user

# Blueprint for authentication routes
auth_bp = Blueprint("auth", __name__)


# -------------------
# REGISTER
# -------------------
@auth_bp.route("/register", methods=["POST"])
def register():

    # Retrieve username from request payload
    data = request.get_json()
    username = data.get("username")

    # Validate that username is provided
    if not username:
        # Return error response if username is missing
        return jsonify({
            "success": False,
            "message": "Username required"
        }), 400

    # Attempt to register user and capture result
    result = register_user(username)

    # AUTO LOGIN AFTER REGISTER
    if result["success"]:
        session["username"] = username

    return jsonify(result)


# -------------------
# LOGIN
# -------------------
@auth_bp.route("/login", methods=["POST"])
def login():

    # Retrieve username from request payload
    data = request.get_json()
    username = data.get("username")

    # Validate that username is provided
    result = login_user(username)

    if result["success"]:
        session["username"] = username

    return jsonify(result)


# -------------------
# CURRENT USER
# -------------------
@auth_bp.route("/me", methods=["GET"])
def me():

    user = session.get("username") # Get username from session to check if user is logged in

    if not user:
        return jsonify({"logged_in": False})
    
    # Return basic user info
    return jsonify({
        "logged_in": True,
        "user": user
    })


# -------------------
# LOGOUT
# -------------------
@auth_bp.route("/logout", methods=["POST"])
def logout():

    session.clear()  # Clear entire session to ensure all user data is removed on logout
    # Clear session to log out user
    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    })