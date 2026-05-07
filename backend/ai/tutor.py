import os
import ast
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def is_valid_python(code):
    try:
        ast.parse(code)
        return True
    except:
        return False


def analyse_code(code, hint_level=0, username="Student"):

    syntax_ok = is_valid_python(code)

    # -------------------------
    # HARD CORRECTNESS CHECK
    # -------------------------
    if syntax_ok and "if" in code and ":" in code:
        # VERY BASIC heuristic example
        # (you can expand later with AST logic trees)
        is_probably_correct = True
    else:
        is_probably_correct = False

    # -------------------------
    # IF CORRECT → RETURN EARLY
    # -------------------------
    if is_probably_correct and hint_level == 0:
        return {
            "correct": True,
            "message": f"Well done {username}, your code looks correct!\n\nClick next hint for potential imporvements or better understanding",
            "hint": ""
        }

    # -------------------------
    # FORCE DIFFERENT BEHAVIOUR PER LEVEL
    # -------------------------

    if hint_level == 0:
        style = f"""
You are a STRICT tutor.

Rules:
- ONLY say if correct or incorrect
- If correct: "Well done {username}\n\nClick next hint for potential imporvements or better understanding"
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

    prompt = f"""
{style}

Code:
{code}

Return ONLY ONE short message.
No JSON.
No explanation outside message.
"""

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

    except Exception as e:
        return {
            "correct": False,
            "message": f"Sorry {username}, I couldn't analyse your code."
        }