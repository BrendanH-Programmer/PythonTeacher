from flask import Flask, send_from_directory, session
from flask_cors import CORS
from backend.routes.lesson_routes import lesson_bp
from backend.routes.auth_routes import auth_bp


# -------------------------
# APP SETUP
# -------------------------
app = Flask(__name__, static_folder="../frontend")

# 🔐 Required for sessions (login system)
app.secret_key = "dev-secret-key"

# ✅ Allow frontend to use sessions
CORS(app, supports_credentials=True)

print("Flask app created")


# -------------------------
# REGISTER ROUTES
# -------------------------
app.register_blueprint(auth_bp, url_prefix="/auth")

# Optional (only if chat still exists)
# app.register_blueprint(chat_bp)


# -------------------------
# FRONTEND SERVING
# -------------------------
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)


# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True)