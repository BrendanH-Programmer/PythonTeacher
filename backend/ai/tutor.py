import os
from openai import OpenAI, api_key


def analyse_code(code):

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "feedback": "API key not found.",
            "suggestion": "Check your .env file and load_dotenv()."
        }

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are a Python tutor helping a beginner.

Analyse this code:

{code}

Rules:
- Be clear and simple
- Do NOT overwhelm
- Give short explanation
- Then give 1 improvement suggestion

Format EXACTLY like:

Feedback: <your feedback>
Suggestion: <your suggestion>
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.choices[0].message.content

        feedback = ""
        suggestion = ""

        if "Suggestion:" in text:
            parts = text.split("Suggestion:")
            feedback = parts[0].replace("Feedback:", "").strip()
            suggestion = parts[1].strip()
        else:
            feedback = text.strip()

        return {
            "feedback": feedback,
            "suggestion": suggestion
        }

    except Exception as e:
        return {
            "feedback": "Error analysing code.",
            "suggestion": str(e)
        }