from flask import Blueprint, request, jsonify, session
from backend.ai.tutor import analyse_code

ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/api/ai/analyse", methods=["POST"])
def analyse():

    if "username" not in session:
        return jsonify({"success": False}), 401

    data = request.get_json()
    code = data.get("code", "")
    hint_level = data.get("hint_level", 0)

    username = session.get("username", "Student")

    result = analyse_code(
        code,
        hint_level=hint_level,
        username=username
    )

    return jsonify({
        "success": True,
        "correct": result["correct"],
        "message": result["message"]
    })