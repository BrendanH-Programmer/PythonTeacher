from backend.users.user_store import load_users, save_users


def get_progress(username):
    users = load_users()
    user = users.get(username)

    if not user:
        return {}

    return user.get("progress", {
        "last_lesson": 1,
        "last_section": "intro",
        "completed_lessons": []
    })


def update_progress(username, lesson_id, section):
    users = load_users()

    if username not in users:
        return False

    user = users[username]

    if "progress" not in user or not isinstance(user["progress"], dict):
        user["progress"] = {
            "last_lesson": 1,
            "last_section": "intro",
            "completed_lessons": []
        }

    progress = user["progress"]

    # update last position
    progress["last_lesson"] = lesson_id
    progress["last_section"] = section

    save_users(users)
    return True