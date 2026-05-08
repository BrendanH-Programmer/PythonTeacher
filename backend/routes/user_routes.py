from flask import Blueprint, jsonify, session, request

from backend.users.user_store import (
    load_users,
    save_users
)

from backend.users.progress_service import (
    get_progress,
    build_lesson_status
)

user_bp = Blueprint("user", __name__)


@user_bp.route("/user/progress", methods=["GET"])
def user_progress():

    username = session.get("username")

    if not username:
        return jsonify({"success": False}), 401

    return jsonify({
        "success": True,
        "progress": get_progress(username)
    })


@user_bp.route("/user/lesson-status", methods=["GET"])
def lesson_status():

    username = session.get("username")

    if not username:
        return jsonify({"success": False}), 401

    progress = get_progress(username)

    return jsonify({
        "success": True,
        "progress": progress,
        "lessons": build_lesson_status(progress)
    })


@user_bp.route("/user/dashboard", methods=["GET"])
def dashboard():

    username = session.get("username")

    if not username:
        return jsonify({"success": False}), 401

    progress = get_progress(username)
    lessons = build_lesson_status(progress)

    next_lesson = next(
        (l["id"] for l in lessons if l["unlocked"] and not l["completed"]),
        None
    )

    return jsonify({
        "success": True,
        "progress": progress,
        "lessons": lessons,
        "next_lesson": next_lesson
    })

# -------------------------
# GET THEME
# -------------------------
@user_bp.route("/user/theme", methods=["GET"])
def get_theme():

    username = session.get("username")

    if not username:
        return jsonify({"success": False}), 401

    users = load_users()

    user = users.get(username)

    if not user:
        return jsonify({"success": False}), 404

    return jsonify({
        "success": True,
        "theme": user.get("theme", "dark")
    })


# -------------------------
# SAVE THEME
# -------------------------
@user_bp.route("/user/theme", methods=["POST"])
def save_theme():

    username = session.get("username")

    if not username:
        return jsonify({"success": False}), 401

    data = request.get_json()

    theme = data.get("theme", "dark")

    if theme not in ["light", "dark"]:
        return jsonify({"success": False}), 400

    users = load_users()

    if username not in users:
        return jsonify({"success": False}), 404

    users[username]["theme"] = theme

    save_users(users)

    return jsonify({
        "success": True
    })