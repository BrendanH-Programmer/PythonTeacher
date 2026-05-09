#-------------------------
# USER ROUTES
# Handles retrieval of user progress and dashboard data
#-------------------------
from flask import Blueprint, jsonify, session, request

# Import user data management functions for handling user progress and theme preferences
from backend.users.user_store import (
    load_users,
    save_users
)

# Import progress service functions for managing user progress and lesson status
from backend.users.progress_service import (
    get_progress,
    build_lesson_status
)

# Blueprint for user-related routes
user_bp = Blueprint("user", __name__)

# -------------------------
# USER PROGRESS
# Retrieves the user's current progress in the course
# -------------------------
@user_bp.route("/user/progress", methods=["GET"])
def user_progress():

    # Get username from session to identify user for progress retrieval
    username = session.get("username")

    # Validate that user is logged in before allowing access to progress data
    if not username:
        return jsonify({"success": False}), 401

    # Retrieve user progress using progress service and return structured response to frontend
    return jsonify({
        "success": True,
        "progress": get_progress(username)
    })

# -------------------------
# LESSON STATUS
# Provides detailed status of all lessons for the user
# -------------------------
@user_bp.route("/user/lesson-status", methods=["GET"])
def lesson_status():

    # Get username from session to identify user for lesson status retrieval
    username = session.get("username")

    # Validate that user is logged in before allowing access to lesson status data
    if not username:
        return jsonify({"success": False}), 401

    # Retrieve user progress and build lesson status using progress service, return structured response to frontend
    progress = get_progress(username)

    # Return both raw progress data and computed lesson status to frontend for dashboard display
    return jsonify({
        "success": True,
        "progress": progress,
        "lessons": build_lesson_status(progress)
    })

# -------------------------
# USER DASHBOARD
# Provides user progress and next lesson info for dashboard display
# -------------------------
@user_bp.route("/user/dashboard", methods=["GET"])
def dashboard():

    # Get username from session to identify user for dashboard data retrieval
    username = session.get("username")

    # Validate that user is logged in before allowing access to dashboard data
    if not username:
        return jsonify({"success": False}), 401

    # Retrieve user progress and build lesson status using progress service, return structured response to frontend for dashboard display
    progress = get_progress(username)
    lessons = build_lesson_status(progress)

    # Determine the next lesson for the user based on their progress, return this info to frontend for dashboard display
    next_lesson = next(
        (l["id"] for l in lessons if l["unlocked"] and not l["completed"]),
        None
    )

    # Return structured dashboard data including progress, lesson status, and next lesson info to frontend for rendering
    return jsonify({
        "success": True,
        "progress": progress,
        "lessons": lessons,
        "next_lesson": next_lesson
    })

# -------------------------
# GET THEME
# Retrieves the user's theme preference (light/dark)
# -------------------------
@user_bp.route("/user/theme", methods=["GET"])
def get_theme():

    # Get username from session to identify user for theme retrieval
    username = session.get("username")

    # Validate that user is logged in before allowing access to theme data
    if not username:
        return jsonify({"success": False}), 401

    # Load user data and retrieve theme preference, return structured response to frontend for theme application
    users = load_users()

    # Validate that user exists in data store before attempting to retrieve theme preference
    user = users.get(username)

    # Return user's theme preference if it exists, otherwise default to "dark" theme for frontend rendering
    if not user:
        return jsonify({"success": False}), 404

    # Return user's theme preference if it exists, otherwise default to "dark" theme for frontend rendering
    return jsonify({
        "success": True,
        "theme": user.get("theme", "dark")
    })


# -------------------------
# SAVE THEME
# Saves the user's theme preference (light/dark) to their profile
# -------------------------
@user_bp.route("/user/theme", methods=["POST"])
def save_theme():

    # Get username from session to identify user for theme update
    username = session.get("username")

    # Validate that user is logged in before allowing theme updates
    if not username:
        return jsonify({"success": False}), 401

    # Retrieve theme preference from request payload and validate input before saving to user profile, return structured response to frontend indicating success or failure of theme update operation
    data = request.get_json()

    #   Extract theme preference from request data, default to "dark" if not provided, and validate that it is either "light" or "dark" before proceeding with update
    theme = data.get("theme", "dark")

    # Validate that provided theme preference is valid (either "light" or "dark"), return error response if invalid input is detected
    if theme not in ["light", "dark"]:
        return jsonify({"success": False}), 400

    # Load user data and validate that user exists before attempting to update theme preference, return error response if user is not found
    users = load_users()

    # Validate that user exists in data store before attempting to update theme preference, return error response if user is not found
    if username not in users:
        return jsonify({"success": False}), 404

    # Update user's theme preference in data store and save changes, return structured response to frontend indicating success of theme update operation
    users[username]["theme"] = theme

    # Save updated user data back to data store to persist theme preference change
    save_users(users)

    # Return success response to frontend indicating that theme preference was successfully updated
    return jsonify({
        "success": True
    })