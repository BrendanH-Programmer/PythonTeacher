AI Python Tutor

An interactive beginner-friendly Python learning platform built with Flask, JavaScript, HTML, and CSS.

This project was designed to help complete beginners learn Python programming step-by-step through structured lessons, guided practice, validation, hints, and progress tracking.

Features:
Learning System:
    10 structured beginner Python lessons
    Section-based lesson flow:
        Introduction
        Learning Outcomes
        Guided Demo
        Practice Task
        Review
    Lesson locking/unlocking progression system
    Resume learning from last section
    Continue learning dashboard card

Code Validation:
    AST-based Python code analysis
    Secure validation without executing user code
    Lesson-specific validation logic
    Detects:
        print statements
        variables
        loops
        functions
        lists
        conditionals
        calculator operators
    Prevents incorrect shortcut solutions

User System:
    Username login
    Session authentication using Flask sessions
    Individual progress tracking per user
    Persistent lesson progress saving
    Persistent theme saving

User Experience:
    Fully responsive mobile-friendly interface
    Professional modern UI
    Dark mode / light mode
    Theme persistence across pages
    Hint system for coding exercises
    Clean navigation system
    Locked lesson protection

Technologies Used:
    Backend
    Python 3
    Flask
    Frontend
    HTML5
    CSS3
    JavaScript (Vanilla JS)
    Python Modules
    ast
    json
    flask
    pathlib

Project Structure:
PythonTeacher/
│
├── backend/
│   ├── app.py
│   ├── auth/
│   │   └── auth_service.py
│   │
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── user_routes.py
│   │   ├── lesson_routes.py
│   │   └── ai_routes.py
│   │
│   ├── ai/
│   │   ├── lesson_validator.py
│   │   └── tutor.py
│   │
│   ├── users/
│   │   ├── user_store.py
│   │   └── progress_service.py
│   │
│   └── data/
│       └── lessons.py
│       └── users.json
│
├── frontend/
│   ├── index.html
│   ├── lesson.html
│   ├── login.html
│   │
│   ├── css/
│   │   └── styles.css
│   │
│   └── js/
│       ├── app.js
│       ├── auth.js
│       ├── lesson_engine.js
│       └── theme.js
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md


Installation:
    1. Clone the Repository
        git clone <https://github.com/BrendanH-Programmer/PythonTeacher>
        cd PythonTeacher

    2. Create Virtual Environment
        Windows
        python -m venv venv
        venv\Scripts\activate

        Mac/Linux
        python3 -m venv venv
        source venv/bin/activate

    3. Install Dependencies
        pip install -r requirements.txt

Running the Application:
    Start the Flask server:
        python -m backend.app

    The application will run at:
    http://127.0.0.1:5000

Default User Data:
    Users are stored inside:

        backend/data/users.json

Example structure:

{
    "Brendan": {
        "progress": {
            "last_lesson": 0,
            "last_section": "intro",
            "completed_lessons": [
                1,
            ],
            "lessons": {
                "1": "review",
            }
        },
        "theme": "dark"
    }
}

Lesson System:
    Each lesson contains:
        title
        order
        validation rules
        intro content
        outcomes
        guided demo
        practice task
        review summary

    Lessons are stored inside:
        backend/data/lessons.py

Validation System:
    The project uses Python AST parsing to safely analyse code submissions:
        Validation includes:
            syntax checking
            structure checking
            operator checking
            variable checking
            loop checking
            conditional checking

    File:
        backend/ai/lesson_validation.py

Theme System:
    The application supports:
        Dark mode
        Light mode
        Theme persistence per user
    Theme data is stored in the user JSON file.

Security Features:
    Session-based authentication
    Protected API routes
    Lesson access validation
    Safe AST parsing
    No direct code execution

API Routes:
    Authentication:
        Route	Method	Purpose
        /auth/login	POST	Login user
        /auth/logout	POST	Logout user
        /auth/me	GET	Check session
    Lessons:
    Route	Method	Purpose
        /api/lesson/<id>/section/<section>	GET	Get lesson section
        /api/lesson/validate	POST	Validate code
        /api/lesson/progress	POST	Save progress
    User:
        Route	Method	Purpose
        /api/user/dashboard	GET	Dashboard data
        /api/user/progress	GET	User progress
        /api/user/lesson-status	GET	Lesson unlock states
        /api/user/theme	GET	Get saved theme
        /api/user/theme	POST	Save theme

Responsive Design:
    The platform supports:
        Desktop
        Tablets
        Mobile devices

    Features include:
        Flexible layouts
        Responsive buttons
        Mobile navigation stacking
        Scroll-safe content boxes

Future Improvements:
    Possible future enhancements include:
        Achievement badges
        XP/level system
        Leaderboards
        Multiple programming languages
        Teacher dashboard
        Database integration
        Email accounts
        Password hashing
        Deployment to cloud hosting

Known Limitations:
    Uses JSON storage instead of a database
    No password encryption
    Intended for educational/demo purposes
    Flask development server only

Author
    Created by Brendan Henderson
    Software Engineering Project

License
    This project is intended for educational use.