# -------------------------
# AI TUTOR SERVICE
# Handles code analysis and hint generation using AI, including syntax checking and lesson-specific validation
# -------------------------
import os
import ast
from openai import OpenAI

# -------------------------
# IMPORTS
# -------------------------
from backend.ai.lesson_validator import validate_lesson
from backend.data.lessons import LESSONS

# -------------------------
# INITIALISE OPENAI CLIENT
# -------------------------
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
# Analyzes the user's code submission, checks for syntax errors, validates it against the lesson requirements, and generates hints based on the specified hint level
# -------------------------
def analyse_code(code, hint_level=0, username="Student", lesson_id=None):

    syntax_ok = is_valid_python(code)

    lesson = None

    try:
        lesson = LESSONS.get(int(lesson_id))
    except:
        lesson = None

    # -------------------------
    # FIXED SAFETY CHECK (was crashing before)
    # This ensures that if the lesson ID is invalid or the lesson cannot be found, the function will return a structured response indicating that the lesson was not found, rather than crashing the application, this is important for maintaining a smooth user experience and providing clear feedback when there are issues with the lesson data
    # -------------------------
    if lesson_id is None or lesson is None:
        return {
            "correct": False,
            "message": "Lesson not found. Please reload the page."
        }

    # -------------------------
    # LESSON VALIDATION
    # Validates the user's code against the specific requirements of the lesson, this is done after confirming that the code is syntactically correct to ensure that we are providing feedback on the actual task requirements rather than syntax errors, this allows for more targeted feedback and hints based on the user's progress in the lesson
    # -------------------------
    task_complete = False

    if lesson:
        task_complete = validate_lesson(code, lesson)

    # -------------------------
    # SUCCESS
    # If the code is syntactically correct and completes the task, return a success message, this is the ideal outcome for the user and indicates that they have successfully completed the lesson requirements
    # -------------------------
    if syntax_ok and task_complete and hint_level == 0:

        return {
            "correct": True,
            "message": f"Well done {username}, you completed the task!",
            "hint": ""
        }

    # -------------------------
    # VALID PYTHON BUT WRONG TASK
    # If the code is syntactically correct but does not complete the task, return a message indicating that the code is valid but does not meet the lesson requirements, this provides feedback to the user that they are on the right track with their coding but need to focus on meeting the specific requirements of the lesson to successfully complete it
    # -------------------------
    if syntax_ok and not task_complete and hint_level == 0:

        lesson_title = "this lesson"

        if lesson and isinstance(lesson, dict):
            lesson_title = lesson.get("title", "this lesson")

        # -------------------------
        # FIXED MESSAGE (was giving a generic message before, now includes lesson title for more specific feedback)
        # This provides more specific feedback to the user by including the title of the lesson they are working on, this helps the user understand that while their code is valid Python, it does not meet the specific requirements of the lesson they are trying to complete, and encourages them to review the lesson material and focus on completing the designated assignment to successfully finish the lesson
        # -------------------------
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
    # Defines different tutor styles based on the hint level, this allows for a progressive hint system where the feedback becomes more detailed and guiding as the user requests more hints, this is designed to encourage learning and problem-solving while providing appropriate levels of assistance based on the user's needs
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
    # Constructs a prompt for the AI based on the specified tutor style, the lesson context, and the user's code submission, this prompt is designed to elicit a response from the AI that provides feedback and hints in line with the defined tutor style, while also taking into account the specific requirements of the lesson and the user's progress, this allows for a more personalized and effective tutoring experience that adapts to the user's needs and encourages learning through guided feedback
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
    # Sends the constructed prompt to the AI and retrieves the response, this is where the AI processes the user's code submission in the context of the lesson and the defined tutor style to generate feedback and hints that are tailored to the user's needs, this allows for a dynamic and interactive tutoring experience that can adapt to different levels of user understanding and provide appropriate guidance based on their progress in the lesson
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

        # Extract the message content from the AI response and return it in a structured format, this message will be used as feedback for the user based on the defined tutor style and the analysis of their code submission, providing them with guidance and hints to help them progress through the lesson
        message = response.choices[0].message.content.strip()

        # -------------------------
        # FIXED RESPONSE HANDLING (was not handling different hint levels properly before, now returns
        # the AI-generated message for all hint levels, this ensures that users receive appropriate feedback and hints based on their requests, rather than only receiving a message at certain hint levels, this is important for maintaining a consistent and helpful tutoring experience as users progress through the lesson and request different levels of assistance
        # -------------------------
        return {
            "correct": False,
            "message": message,
            "hint_level": hint_level
        }

    # -------------------------
    # ERROR HANDLING
    # Catches any exceptions that occur during the AI analysis process and returns a structured response indicating that the analysis could not be completed, this is important for maintaining a smooth user experience and providing clear feedback when there are issues with the AI service or the analysis process, rather than crashing the application or leaving the user without any feedback
    # -------------------------
    except Exception as e:
        return {
            "correct": False,
            "message": f"Sorry {username}, I couldn't analyse your code."
        }