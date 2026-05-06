from flask import Blueprint, request, jsonify, session
from backend.ai.tutor import analyse_code

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/api/ai/analyse", methods=["POST"])
def analyse():

    if "username" not in session:
        return jsonify({"success": False, "error": "Not logged in"}), 401

    data = request.get_json()
    code = data.get("code")

    if not code:
        return jsonify({"success": False, "error": "No code provided"}), 400

    result = analyse_code(code)

    return jsonify({
        "success": True,
        "feedback": result["feedback"],
        "suggestion": result["suggestion"]
    })