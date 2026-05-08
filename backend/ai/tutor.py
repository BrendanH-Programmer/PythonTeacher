import os
import ast
from openai import OpenAI

from backend.ai.lesson_validator import validate_lesson
from backend.data.lessons import LESSONS

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -------------------------
# PYTHON SYNTAX CHECK
# -------------------------
def is_valid_python(code):

    try:
        ast.parse(code)
        return True

    except:
        return False


# -------------------------
# MAIN ANALYSIS
# -------------------------
def analyse_code(code, hint_level=0, username="Student", lesson_id=None):

    syntax_ok = is_valid_python(code)

    lesson = None  # ✅ FIX: define BEFORE using it

    try:
        lesson = LESSONS.get(int(lesson_id))
    except:
        lesson = None

    # -------------------------
    # FIXED SAFETY CHECK (was crashing before)
    # -------------------------
    if lesson_id is None or lesson is None:
        return {
            "correct": False,
            "message": "Lesson not found. Please reload the page."
        }

    # -------------------------
    # LESSON VALIDATION
    # -------------------------
    task_complete = False

    if lesson:
        task_complete = validate_lesson(code, lesson)

    # -------------------------
    # SUCCESS
    # -------------------------
    if syntax_ok and task_complete and hint_level == 0:

        return {
            "correct": True,
            "message": f"Well done {username}, you completed the task!",
            "hint": ""
        }

    # -------------------------
    # VALID PYTHON BUT WRONG TASK
    # -------------------------
    if syntax_ok and not task_complete and hint_level == 0:

        lesson_title = "this lesson"

        if lesson and isinstance(lesson, dict):
            lesson_title = lesson.get("title", "this lesson")

        return {
            "correct": False,
            "message":
                f"Your code is valid Python {username}, "
                f"but it does not complete the task for "
                f"'{lesson_title}'. "
                f"Complete the designated assignment to finish the lesson."
        }

    # -------------------------
    # TUTOR STYLES
    # -------------------------
    if hint_level == 0:
        style = f"""
You are a STRICT tutor.

Rules:
- ONLY say if correct or incorrect
- If correct: "Well done {username}, you completed the task!"
- If incorrect: "Ooo {username}, there is a mistake somewhere"
- NO explanation
"""

    elif hint_level == 1:
        style = f"""
You are a gentle tutor.

Rules:
- Give ONLY a vague hint
- Example style: "mmm {username}, something feels off..."
- DO NOT mention operators or exact bug
"""

    elif hint_level == 2:
        style = f"""
You are a guiding tutor.

Rules:
- Point at the AREA of the problem (logic / condition / structure)
- DO NOT give fix
- Encourage thinking
"""

    else:
        style = f"""
You are a strong tutor.

Rules:
- Ask a question that leads to the answer
- Focus on reasoning about conditions
"""
    # -------------------------
    # AI PROMPT
    # -------------------------
    prompt = f"""
{style}

lesson:
{lesson.get("title") if lesson else "Python"}

Code:
{code}

Return ONLY ONE short message.
No JSON.
No explanation outside message.
"""

    # -------------------------
    # AI RESPONSE
    # -------------------------
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a Python tutor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )

        message = response.choices[0].message.content.strip()

        return {
            "correct": False,
            "message": message,
            "hint_level": hint_level
        }

    # -------------------------
    # ERROR HANDLING
    # -------------------------
    except Exception as e:
        return {
            "correct": False,
            "message": f"Sorry {username}, I couldn't analyse your code."
        }