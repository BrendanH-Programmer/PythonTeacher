from flask import Blueprint, jsonify, session
from backend.users.user_store import load_users
from backend.users.progress_service import build_lesson_status

user_bp = Blueprint("user", __name__)


# -------------------------
# GET CURRENT USER PROGRESS (RAW)
# -------------------------
@user_bp.route("/user/progress", methods=["GET"])
def user_progress():

    username = session.get("user")

    if not username:
        return jsonify({"success": False}), 401

    users = load_users()
    user = users.get(username)

    if not user:
        return jsonify({
            "success": True,
            "progress": {
                "last_lesson": 1,
                "last_section": "intro",
                "completed_lessons": []
            }
        })

    return jsonify({
        "success": True,
        "progress": user.get("progress", {
            "last_lesson": 1,
            "last_section": "intro",
            "completed_lessons": []
        })
    })


# -------------------------
# LESSON STATUS (PRIMARY FRONTEND ENDPOINT)
# -------------------------
@user_bp.route("/user/lesson-status", methods=["GET"])
def lesson_status():

    username = session.get("user")

    if not username:
        return jsonify({"success": False}), 401

    users = load_users()
    user = users.get(username, {})

    progress = user.get("progress", {
        "last_lesson": 1,
        "last_section": "intro",
        "completed_lessons": []
    })

    return jsonify({
        "success": True,
        "progress": progress,
        "lessons": build_lesson_status(progress)
    })


# -------------------------
# DASHBOARD (optional but useful)
# -------------------------
@user_bp.route("/user/dashboard", methods=["GET"])
def dashboard():

    username = session.get("user")

    if not username:
        return jsonify({"success": False}), 401

    users = load_users()
    user = users.get(username, {})

    progress = user.get("progress", {
        "last_lesson": 1,
        "last_section": "intro",
        "completed_lessons": []
    })

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