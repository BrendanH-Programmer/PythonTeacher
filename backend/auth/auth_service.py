from backend.users.user_store import get_user, add_user


def register_user(username):
    """
    Registers a new user (username only system)
    """

    if get_user(username):
        return {
            "success": False,
            "message": "User already exists"
        }

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


def login_user(username):
    """
    Logs in an existing user
    """

    user = get_user(username)

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }

    return {
        "success": True,
        "message": "Login successful",
        "user": {
            "username": username
        }
    }