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
            "lessons": {},
            "completed_lessons": []
        }

    return user.get("progress", {
        "lessons": {},
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

    progress = user.setdefault("progress", {})

    # 🔥 SAFE INITIALISATION (IMPORTANT FIX)
    if "lessons" not in progress:
        progress["lessons"] = {}

    if "completed_lessons" not in progress:
        progress["completed_lessons"] = []

    # store per-lesson progress
    progress["lessons"][str(lesson_id)] = section

    # completion logic
    if section == "review":
        if lesson_id not in progress["completed_lessons"]:
            progress["completed_lessons"].append(lesson_id)

    save_users(users)
    return True

# -------------------------
# UNLOCK LOGIC (ONLY SOURCE OF TRUTH)
# -------------------------
def is_unlocked(completed, lesson_id):

    if lesson_id == 1:
        return True

    return (lesson_id - 1) in completed


# -------------------------
# BUILD LESSON STATUS (FRONTEND READY)
# -------------------------
def build_lesson_status(progress):

    completed = set(map(int, progress.get("completed_lessons", [])))
    last_lesson = int(progress.get("last_lesson", 1))

    lessons_status = []

    for lesson_id, lesson in LESSONS.items():

        lesson_id = int(lesson_id)

        is_completed = lesson_id in completed
        unlocked = is_unlocked(completed, lesson_id)
        is_current = (lesson_id == last_lesson and not is_completed)

        lessons_status.append({
            "id": lesson_id,
            "title": lesson["title"],
            "completed": is_completed,
            "unlocked": unlocked,
            "current": is_current
        })

    return lessons_status