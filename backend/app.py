from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))

from backend.routes.auth_routes import auth_bp
from backend.routes.lesson_routes import lesson_bp
from backend.routes.user_routes import user_bp
from backend.routes.ai_routes import ai_bp

app = Flask(__name__, static_folder="../frontend")

app.config.update(
    SESSION_COOKIE_SAMESITE="Lax",   # important
    SESSION_COOKIE_SECURE=False      # must be False for local dev
)

app.secret_key = "dev-secret-key"

CORS(
    app,
    supports_credentials=True,
    origins=[
        "http://127.0.0.1:5000",
        "http://localhost:5000"
    ]
)

print("Flask app created")

# ROUTES
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(lesson_bp, url_prefix="/api")
app.register_blueprint(user_bp, url_prefix="/api")
app.register_blueprint(ai_bp)

@app.route("/")
def home():
    return send_from_directory(app.static_folder, "login.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)


if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True)