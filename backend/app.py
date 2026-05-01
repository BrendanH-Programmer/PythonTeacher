from flask import Flask, send_from_directory
from flask_cors import CORS

from backend.routes.auth_routes import auth_bp
from backend.routes.lesson_routes import lesson_bp

app = Flask(__name__, static_folder="../frontend")

app.secret_key = "dev-secret-key"

CORS(app, supports_credentials=True)

print("Flask app created")

# ROUTES
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(lesson_bp, url_prefix="/api")


@app.route("/")
def home():
    return send_from_directory(app.static_folder, "login.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)


if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True)