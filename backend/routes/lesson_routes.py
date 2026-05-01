from flask import Blueprint, jsonify, session
from backend.data.lessons import LESSONS

lesson_bp = Blueprint("lessons", __name__)


# -------------------------
# GET ALL LESSONS
# -------------------------
@lesson_bp.route("/lessons", methods=["GET"])
def get_all_lessons():
    return jsonify({
        "success": True,
        "lessons": [
            {
                "id": k,
                "title": v["title"],
                "difficulty": v["difficulty"]
            }
            for k, v in LESSONS.items()
        ]
    })


# -------------------------
# GET SINGLE LESSON
# -------------------------
@lesson_bp.route("/lesson/<int:lesson_id>", methods=["GET"])
def get_lesson(lesson_id):

    lesson = LESSONS.get(lesson_id)

    if not lesson:
        return jsonify({
            "success": False,
            "message": "Lesson not found"
        }), 404

    return jsonify({
        "success": True,
        "lesson": lesson
    })


# -------------------------
# PROGRESS UPDATE
# -------------------------
@lesson_bp.route("/lesson/complete/<int:lesson_id>", methods=["POST"])
def complete_lesson(lesson_id):

    username = session.get("user")

    if not username:
        return jsonify({
            "success": False,
            "message": "Not logged in"
        }), 401

    from backend.users.user_store import get_user, save_users

    users = get_user(username)

    if "progress" not in users:
        users["progress"] = []

    if lesson_id not in users["progress"]:
        users["progress"].append(lesson_id)

    save_users(load_users := __import__("backend.users.user_store", fromlist=["load_users"]).load_users())

    return jsonify({
        "success": True,
        "message": f"Lesson {lesson_id} completed"
    })