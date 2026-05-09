# =========================================================
# AI ANALYSIS ROUTES
# Handles code submission analysis and hint generation
# =========================================================
from flask import Blueprint, request, jsonify, session
from backend.ai.tutor import analyse_code

ai_bp = Blueprint("ai", __name__)

# =========================================================
# ANALYSE CODE ENDPOINT
# Sends user code to AI tutor for validation and feedback
# =========================================================
@ai_bp.route("/api/ai/analyse", methods=["POST"])
def analyse():

    # Ensure user is logged in before allowing AI usage
    if "username" not in session:
        return jsonify({"success": False}), 401

    # Retrieve request payload from frontend
    data = request.get_json()

    # Extract submitted code
    code = data.get("code", "")

    # Extract hint level (used for progressive hint system)
    hint_level = data.get("hint_level", 0)

    # Extract lesson context for lesson-specific validation    
    lesson_id = data.get("lesson_id") 

    # Get username from session (fallback included for safety)
    username = session.get("username", "Student")

    # Send code to AI tutor for analysis
    result = analyse_code(
        code,
        hint_level=hint_level,
        username=username,
        lesson_id=lesson_id
    )

    # Return structured response to frontend
    return jsonify({
        "success": True,
        "correct": result["correct"],
        "message": result["message"]
    })