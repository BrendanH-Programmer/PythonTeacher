from flask import Blueprint, jsonify, session, request
from backend.data.lessons import LESSONS
from backend.users.user_store import load_users, save_users

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
                "order": v["order"]
            }
            for k, v in LESSONS.items()
        ]
    })


# -------------------------
# GET LESSON SECTION
# -------------------------
@lesson_bp.route("/lesson/<int:lesson_id>/section/<section>", methods=["GET"])
def get_lesson_section(lesson_id, section):

    lesson = LESSONS.get(lesson_id)

    if not lesson:
        return jsonify({"success": False, "message": "Lesson not found"}), 404

    section_data = lesson["sections"].get(section)

    if not section_data:
        return jsonify({"success": False, "message": "Section not found"}), 404

    return jsonify({
        "success": True,
        "lesson_id": lesson_id,
        "lesson_title": lesson["title"],
        "section": section,
        "data": section_data
    })


# -------------------------
# SAVE PROGRESS
# -------------------------
@lesson_bp.route("/lesson/progress", methods=["POST"])
def save_progress():

    data = request.get_json()
    username = session.get("user")

    if not username:
        return jsonify({"success": False}), 401

    lesson_id = data.get("lesson_id")
    section = data.get("section")

    users = load_users()
    user = users[username]

    progress = user.get("progress", {
        "last_lesson": 1,
        "last_section": "intro",
        "completed_lessons": []
    })

    progress["last_lesson"] = lesson_id
    progress["last_section"] = section

    # mark completion
    if section == "review":
        if lesson_id not in progress["completed_lessons"]:
            progress["completed_lessons"].append(lesson_id)

    user["progress"] = progress

    save_users(users)

    return jsonify({"success": True})

# -------------------------
# RESUME
# -------------------------
@lesson_bp.route("/user/resume", methods=["GET"])
def resume():

    username = session.get("user")

    if not username:
        return jsonify({"success": False}), 401

    users = load_users()
    user = users.get(username)

    if not user:
        return jsonify({"success": False}), 404

    progress = user.get("progress", {})

    return jsonify({
        "success": True,
        "last_lesson": progress.get("last_lesson", 1),
        "last_section": progress.get("last_section", "intro")
    })


# -------------------------
# COMPLETED LESSONS
# -------------------------
@lesson_bp.route("/user/completed", methods=["GET"])
def completed():

    username = session.get("user")

    if not username:
        return jsonify({"success": False}), 401

    users = load_users()
    user = users.get(username, {})

    progress = user.get("progress", {})

    return jsonify({
        "success": True,
        "completed": progress.get("completed_lessons", [])
    })

# -------------------------
# CHECK UNLOCKED
# -------------------------
def is_lesson_unlocked(username, lesson_id):
    users = load_users()
    user = users.get(username)

    if not user:
        return lesson_id == 1

    progress = user.get("progress", {})
    completed = progress.get("completed_lessons", [])

    if lesson_id == 1:
        return True

    return (lesson_id - 1) in completed