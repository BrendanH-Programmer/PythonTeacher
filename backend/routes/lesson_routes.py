from flask import Blueprint, jsonify, session, request
from backend.data.lessons import LESSONS
from backend.users.progress_service import get_progress, update_progress

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
        return jsonify({"success": False, "message": "Not logged in"}), 401

    lesson_id = data.get("lesson_id")
    section = data.get("section")

    success = update_progress(username, lesson_id, section)

    return jsonify({
        "success": success,
        "message": "Progress updated"
    })


# -------------------------
# GET USER PROGRESS
# -------------------------
@lesson_bp.route("/user/progress", methods=["GET"])
def user_progress():

    username = session.get("user")

    if not username:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    progress = get_progress(username)

    return jsonify({
        "success": True,
        "progress": progress
    })

# -------------------------
# USER PROGRESSION LOCKED ROUTE
# -------------------------

@lesson_bp.route("/lesson/<int:lesson_id>/next", methods=["GET"])
def next_section():
    username = session.get("user")

    if not username:
        return jsonify({"error": "not logged in"}), 401