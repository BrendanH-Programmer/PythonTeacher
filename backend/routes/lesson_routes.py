# -------------------------
# LESSON ROUTES
# Handles retrieval of lesson content and saving user progress
# -------------------------
from flask import Blueprint, jsonify, session, request
from backend.data.lessons import LESSONS
from backend.users.progress_service import update_progress

# Blueprint for lesson-related routes
lesson_bp = Blueprint("lessons", __name__)


# -------------------------
# GET ALL LESSONS
# Provides a list of all lessons with basic information for frontend display
# -------------------------
@lesson_bp.route("/lessons", methods=["GET"])
def get_all_lessons():

    # Return list of all lessons with basic info for frontend display
    return jsonify({
        "success": True,
        "lessons": [
            {
                "id": int(k),
                "title": v["title"],
                "order": v["order"]
            }
            # Convert lesson ID to int for frontend consistency
            for k, v in LESSONS.items()
        ]
    })


# -------------------------
# GET LESSON SECTION
# Retrieves specific section of a lesson based on lesson ID and section name
# -------------------------
@lesson_bp.route("/lesson/<int:lesson_id>/section/<section>", methods=["GET"])
def get_lesson_section(lesson_id, section):

    # Retrieve lesson data based on lesson ID and section name, return structured response for frontend rendering
    lesson = LESSONS.get(lesson_id)

    # Validate that lesson and section exist, return appropriate error messages if not found
    if not lesson:
        return jsonify({"success": False, "message": "Lesson not found"}), 404

    # Validate that requested section exists within the lesson
    section_data = lesson["sections"].get(section)

    if not section_data:
        return jsonify({"success": False, "message": "Section not found"}), 404

    # Return lesson section data to frontend for rendering
    return jsonify({
        "success": True,
        "lesson_id": lesson_id,
        "lesson_title": lesson["title"],
        "section": section,
        "data": section_data
    })


# -------------------------
# SAVE PROGRESS (DELEGATED)
# Receives progress updates from frontend and delegates to progress service for handling
# -------------------------
@lesson_bp.route("/lesson/progress", methods=["POST"])
def save_progress():

    # Retrieve progress update data from request payload and delegate to progress service for handling
    data = request.get_json()
    username = session.get("username")

    # Validate that user is logged in before allowing progress updates
    if not username:
        return jsonify({"success": False}), 401

    # Extract lesson ID and section from request data for progress update
    lesson_id = int(data.get("lesson_id"))
    section = data.get("section")

    # Validate that lesson ID and section are provided in request data
    success = update_progress(username, lesson_id, section)

    # Return success status of progress update operation to frontend
    return jsonify({"success": success})