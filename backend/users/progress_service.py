from backend.users.user_store import load_users, save_users
from backend.data.lessons import LESSONS


# -------------------------
# GET PROGRESS
# -------------------------
def get_progress(username):

    users = load_users()
    user = users.get(username)

    if not user:
        return {
            "last_lesson": 1,
            "last_section": "intro",
            "completed_lessons": []
        }

    return user.get("progress", {
        "last_lesson": 1,
        "last_section": "intro",
        "completed_lessons": []
    })


# -------------------------
# UPDATE PROGRESS
# -------------------------
def update_progress(username, lesson_id, section):

    users = load_users()

    if username not in users:
        return False

    user = users[username]

    progress = user.setdefault("progress", {
        "last_lesson": 1,
        "last_section": "intro",
        "completed_lessons": []
    })

    progress["last_lesson"] = lesson_id
    progress["last_section"] = section

    if section == "review":
        if lesson_id not in progress["completed_lessons"]:
            progress["completed_lessons"].append(lesson_id)

    save_users(users)
    return True


# -------------------------
# UNLOCK LOGIC
# -------------------------
def is_lesson_unlocked(progress, lesson_id):

    completed = set(map(int, progress.get("completed_lessons") or []))

    if lesson_id == 1:
        return True

    return (lesson_id - 1) in completed


# -------------------------
# BUILD LESSON STATUS
# -------------------------
def build_lesson_status(progress):

    completed = set(map(int, progress.get("completed_lessons") or []))
    last_lesson = int(progress.get("last_lesson", 1))

    lessons_status = []

    for lesson_id, lesson in LESSONS.items():

        lesson_id = int(lesson_id)

        is_completed = lesson_id in completed
        is_unlocked = is_lesson_unlocked(progress, lesson_id)

        is_current = (
            lesson_id == last_lesson
            and lesson_id not in completed
        )

        lessons_status.append({
            "id": lesson_id,
            "title": lesson["title"],
            "completed": is_completed,
            "unlocked": is_unlocked,
            "current": is_current
        })

    return lessons_status