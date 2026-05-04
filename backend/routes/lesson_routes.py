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
                "id": int(k),
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

    lesson_id = int(data.get("lesson_id"))
    section = data.get("section")

    users = load_users()
    user = users.setdefault(username, {"progress": {}})

    progress = user.setdefault("progress", {})
    progress.setdefault("completed_lessons", [])

    # update last position
    progress["last_lesson"] = lesson_id
    progress["last_section"] = section

    # ONLY mark complete if review reached
    if section == "review":
        if lesson_id not in progress["completed_lessons"]:
            progress["completed_lessons"].append(lesson_id)

    save_users(users)

    return jsonify({"success": True})


# -------------------------
# USER PROGRESS
# -------------------------
@lesson_bp.route("/user/progress", methods=["GET"])
def user_progress():

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
        "progress": progress
    })


# -------------------------
# UNLOCK LOGIC
# -------------------------
def is_lesson_unlocked(username, lesson_id):

    users = load_users()
    user = users.get(username)

    if not user:
        return lesson_id == 1

    progress = user.get("progress", {})
    completed = set(map(int, progress.get("completed_lessons", [])))

    # lesson 1 always unlocked
    if lesson_id == 1:
        return True

    # STRICT RULE: must complete previous lesson
    return (lesson_id - 1) in completed


# -------------------------
# LESSON STATUS
# -------------------------
@lesson_bp.route("/user/lesson-status", methods=["GET"])
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

    completed = set(map(int, progress.get("completed_lessons", [])))
    last_lesson = progress.get("last_lesson", 1)

    lessons_status = []

    for lesson_id, lesson in LESSONS.items():

        lesson_id = int(lesson_id)

        is_completed = lesson_id in completed
        is_unlocked = lesson_id == 1 or (lesson_id - 1) in completed
        is_current = lesson_id == last_lesson and not is_completed

        lessons_status.append({
            "id": lesson_id,
            "title": lesson["title"],
            "completed": is_completed,
            "unlocked": is_unlocked,
            "current": is_current
        })

    return jsonify({
        "success": True,
        "progress": progress,
        "lessons": lessons_status
    })