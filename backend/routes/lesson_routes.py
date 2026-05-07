from flask import Blueprint, jsonify, session, request
from backend.data.lessons import LESSONS
from backend.users.progress_service import update_progress

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
# SAVE PROGRESS (DELEGATED)
# -------------------------
@lesson_bp.route("/lesson/progress", methods=["POST"])
def save_progress():

    data = request.get_json()
    username = session.get("username")

    if not username:
        return jsonify({"success": False}), 401

    lesson_id = int(data.get("lesson_id"))
    section = data.get("section")

    success = update_progress(username, lesson_id, section)

    return jsonify({"success": success})