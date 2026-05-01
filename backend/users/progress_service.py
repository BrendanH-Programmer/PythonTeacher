from backend.users.user_store import load_users, save_users


def get_progress(username):
    users = load_users()
    user = users.get(username)

    if not user:
        return {}

    return user.get("progress", {})


def update_progress(username, lesson_id, section):
    users = load_users()

    if username not in users:
        return False

    user = users[username]

    if "progress" not in user:
        user["progress"] = {}

    lesson_key = str(lesson_id)

    if lesson_key not in user["progress"]:
        user["progress"][lesson_key] = []

    if section not in user["progress"][lesson_key]:
        user["progress"][lesson_key].append(section)

    save_users(users)
    return True