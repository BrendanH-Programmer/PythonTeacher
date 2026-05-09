# -------------------------
# APP SETUP
# This file sets up the Flask application, configures CORS, loads environment variables, and registers the different route blueprints for authentication, lessons, user management, and AI tutoring. It also defines routes for serving the frontend static files and starts the Flask server when the script is run directly. This is the main entry point for the backend application and is responsible for initializing all the necessary components and configurations to ensure that the application runs smoothly and can handle incoming requests appropriately.
# -------------------------
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os

#-------------------------
# IMPORTS
#-------------------------
import logging

# Set logging level to ERROR to reduce console output during development, this helps to focus on important error messages while minimizing less critical logs, making it easier to identify and address issues during the development process
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

#-------------------------
# ENVIRONMENT VARIABLES
# Loads environment variables from a .env file located in the parent directory of the current file, this allows for secure management of sensitive information such as API keys and configuration settings without hardcoding them into the source code, this is important for maintaining security and flexibility in different deployment environments
#-------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# -------------------------
# APP INITIALIZATION
# Initializes the Flask application, configures CORS to allow requests from the specified origins, and
# sets up session cookie settings for security and development purposes, this is the foundational setup for the backend application that allows it to handle incoming requests, manage user sessions, and interact with the frontend application while ensuring that cross-origin requests are properly handled
# -------------------------
from backend.routes.auth_routes import auth_bp
from backend.routes.lesson_routes import lesson_bp
from backend.routes.user_routes import user_bp
from backend.routes.ai_routes import ai_bp

# -------------------------
# ROUTE BLUEPRINTS
# Imports the route blueprints for authentication, lessons, user management, and AI tutoring, and registers them with the Flask application under the appropriate URL prefixes, this modular approach to routing allows for better organization of the codebase and makes it easier to manage different aspects of the application's functionality by grouping related routes together in separate files
# -------------------------
app = Flask(__name__, static_folder="../frontend")

#-------------------------
# SESSION CONFIGURATION
# Configures session cookie settings to enhance security and ensure proper handling of user sessions, this includes
# setting the SameSite attribute to "Lax" to help prevent CSRF attacks while still allowing for necessary cross-origin requests during development, and setting the Secure attribute to False for local development since HTTPS is not typically used in that environment, these settings are important for maintaining a secure and functional user session management system in the application
#-------------------------
app.config.update(
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False      # must be False for local dev
)

#-------------------------
# SECRET KEY
# Sets a secret key for the Flask application, which is used for securely signing the session cookie and other security-related needs, in a production application you would want to use a more secure and randomly generated secret key, and keep it hidden (e.g., in an environment variable) rather than hardcoding it into the source code, this is important for maintaining the security of user sessions and preventing potential attacks that could compromise session data
#-------------------------
app.secret_key = "dev-secret-key"

#-------------------------
# CORS CONFIGURATION
# Configures Cross-Origin Resource Sharing (CORS) for the Flask application to allow requests from
# the specified origins, this is important for enabling communication between the frontend and backend during development, especially when they are served from different origins (e.g., different ports), this configuration allows the frontend to make API requests to the backend without being blocked by the browser's same-origin policy, while still maintaining some level of security by restricting allowed origins
#-------------------------
CORS(
    app,
    supports_credentials=True,
    origins=[
        "http://127.0.0.1:5000",
        "http://localhost:5000"
    ]
)

#-------------------------
# REGISTER BLUEPRINTS
# Registers the imported route blueprints with the Flask application under the appropriate URL prefixes, this allows
# for better organization of the codebase by grouping related routes together in separate files, and makes it easier to manage different aspects of the application's functionality, such as authentication, lesson management, user progress tracking, and AI tutoring, by keeping the route definitions modular and organized
#-------------------------
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(lesson_bp, url_prefix="/api")
app.register_blueprint(user_bp, url_prefix="/api")
app.register_blueprint(ai_bp)

#-------------------------
# STATIC FILES
# Defines routes for serving the frontend static files, including the main entry point (login.html) and any other static assets, this allows the Flask application to serve the frontend application directly, enabling users to access the login page and other frontend resources without needing a separate server for the frontend during development, this is a common setup for full-stack applications where the backend serves both API endpoints and static files for the frontend
#-------------------------
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "login.html")

# Route to serve other static files (e.g., JavaScript, CSS, images) from the frontend directory, this allows the Flask application to handle requests for any static assets that are part of the frontend application, ensuring that all necessary resources are available to the user when they access the frontend through the Flask server
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

#-------------------------
# RUN SERVER
# Starts the Flask server when the script is run directly, this allows the application to listen for incoming requests and serve both the API endpoints and the frontend static files, this is the main entry point for running the backend application during development
#-------------------------
if __name__ == "__main__":
    app.run(debug=False)