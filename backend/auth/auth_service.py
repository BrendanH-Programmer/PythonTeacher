# =========================================================
# USER AUTHENTICATION SERVICE
# Handles user registration and login logic
# =========================================================

from backend.users.user_store import get_user, add_user


# =========================================================
# REGISTER USER
# Creates a new user if they do not already exist
# =========================================================
def register_user(username):

    # Check if user already exists in storage
    if get_user(username):
        return {
            "success": False,
            "message": "User already exists"
        }

    # Create new user with default progress structure
    add_user(username, {
        "progress": {
            "last_lesson": 1,
            "last_section": "intro",
            "completed_lessons": []
        }
    })

    return {
        "success": True,
        "message": "User created successfully"
    }


# =========================================================
# LOGIN USER
# Validates that a user exists in the system
# =========================================================
def login_user(username):

    # Retrieve user from storage
    user = get_user(username)

    # If user does not exist, login fails
    if not user:
        return {
            "success": False,
            "message": "User not found"
        }

    # If user exists, login is successful
    return {
        "success": True,
        "message": "Login successful"
    }