# -------------------------
# PROGRESS SERVICE
# Handles all logic related to user progress tracking, including retrieval, updates, and lesson status computation
# -------------------------
from backend.users.user_store import load_users, save_users
from backend.data.lessons import LESSONS


# -------------------------
# GET PROGRESS
# Retrieves the user's current progress in the course, including completed lessons and last accessed lesson/section
# -------------------------
def get_progress(username):

    # Load user data and retrieve progress information for the specified user, return default progress structure if user is not found or has no progress data
    users = load_users()
    user = users.get(username)

    # Validate that user exists in data store before attempting to retrieve progress information, return default progress structure if user is not found
    if not user:
        return {
            "lessons": {},
            "completed_lessons": []
        }

    # Return user's progress information if it exists, otherwise return default progress structure for frontend rendering
    return user.get("progress", {
        "lessons": {},
        "completed_lessons": []
    })


# -------------------------
# UPDATE PROGRESS
# Updates the user's progress based on the lesson and section they have accessed, handles completion logic for lessons
# -------------------------
def update_progress(username, lesson_id, section):

    # Load user data and validate that user exists before attempting to update progress information, return False if user is not found
    users = load_users()

    # Validate that user exists in data store before attempting to update progress information, return False if user is not found
    if username not in users:
        return False

    # Retrieve user data and initialize progress structure if it does not exist to ensure safe updates to progress information
    user = users[username]

    # SAFE INITIALISATION OF PROGRESS STRUCTURE TO PREVENT KEY ERRORS DURING UPDATES
    progress = user.setdefault("progress", {})

    #  SAFE INITIALISATION
    if "lessons" not in progress:
        progress["lessons"] = {}

    # SAFE INITIALISATION
    if "completed_lessons" not in progress:
        progress["completed_lessons"] = []

    # store per-lesson progress
    progress["lessons"][str(lesson_id)] = section

    # completion logic
    if section == "review":
        if lesson_id not in progress["completed_lessons"]:
            progress["completed_lessons"].append(lesson_id)

    # Save updated user data back to data store to persist progress changes, return True to indicate successful progress update operation
    save_users(users)
    return True

# -------------------------
# UNLOCK LOGIC (ONLY SOURCE OF TRUTH)
# Determines whether a lesson should be unlocked based on the user's completed lessons, ensures that lessons are unlocked in a linear progression to guide the learning experience
# -------------------------
def is_unlocked(completed, lesson_id):

    # The first lesson is always unlocked to allow users to start the course, subsequent lessons require completion of the previous lesson to ensure a structured learning path
    if lesson_id == 1:
        return True

    # For lessons beyond the first, check if the previous lesson has been completed to determine if the current lesson should be unlocked, this enforces a linear progression through the course material
    return (lesson_id - 1) in completed


# -------------------------
# BUILD LESSON STATUS
# Constructs a list of lessons with their completion and unlock status based on the user's progress, this information is used to render the dashboard and guide the user through the course
# -------------------------
def build_lesson_status(progress):

    # Convert completed lessons to a set for efficient lookup when determining lesson status, this allows for quick checks to see if a lesson has been completed when building the status list
    completed = set(map(int, progress.get("completed_lessons", [])))
    last_lesson = int(progress.get("last_lesson", 1))

    # Iterate through all lessons and determine their completion and unlock status based on the user's progress, this information is used to render the dashboard and guide the user through the course
    lessons_status = []

    # Iterate through all lessons defined in the LESSONS data structure to build a comprehensive status list that includes completion, unlock, and current lesson information for each lesson, this ensures that the frontend has all necessary information to render the dashboard accurately
    for lesson_id, lesson in LESSONS.items():

        # Convert lesson ID to int for consistent comparisons when determining lesson status, this ensures that the lesson ID is in the correct format for checking against completed lessons and last accessed lesson
        lesson_id = int(lesson_id)

        # Determine if the lesson is completed by checking if its ID is in the set of completed lessons, this allows us to mark lessons as completed on the dashboard and provide feedback to the user about their progress
        is_completed = lesson_id in completed
        unlocked = is_unlocked(completed, lesson_id)
        is_current = (lesson_id == last_lesson and not is_completed)

        # Append the lesson's status information to the lessons_status list, including its ID, title, completion status, unlock status, and whether it is the current lesson being worked on, this structured information is used by the frontend to render the dashboard and guide the user through their learning journey
        lessons_status.append({
            "id": lesson_id,
            "title": lesson["title"],
            "completed": is_completed,
            "unlocked": unlocked,
            "current": is_current
        })

    # Return the constructed list of lesson statuses to the caller, this information is essential for rendering the dashboard and providing feedback to the user about their progress and which lessons are available to them
    return lessons_status