# -------------------------
# USER STORE
# Handles loading and saving user data to a JSON file, this is a simple implementation for demonstration
# purposes, in a production application you would likely want to use a database for better performance and scalability
# -------------------------
import json
import os

# -------------------------
# USER DATA MANAGEMENT
# Provides functions to load, save, and manage user data stored in a JSON file, this
# includes functions to retrieve user information and add new users, this is a simple file-based approach for demonstration purposes, in a production application you would likely want to use a more robust data storage solution such as a database for better performance and scalability
# -------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
USER_FILE = os.path.join(BASE_DIR, "data", "users.json")

# -------------------------
# USER DATA FUNCTIONS
# Functions to load user data from the JSON file, save user data to the file, retrieve specific user information, and add new users to the data store, these functions provide the basic CRUD operations needed to manage user data in a simple file-based system, allowing for user registration, authentication, and progress tracking in the application
# -------------------------
def load_users():
    if not os.path.exists(USER_FILE):
        return {}

    # Load user data from the JSON file, if the file is empty or contains invalid JSON, return an empty dictionary to prevent errors when accessing user data, this ensures that the application can handle cases where the user data file is not properly initialized without crashing
    with open(USER_FILE, "r") as f:
        try:
            # Load user data from the JSON file, if the file is empty or contains invalid JSON, return an empty dictionary to prevent errors when accessing user data, this ensures that the application can handle cases where the user data file is not properly initialized without crashing
            return json.load(f)
        except json.JSONDecodeError:
            return {}

# --------------------------
# SAVE USERS
# Saves the provided user data to the JSON file, this function ensures that the user data is properly written to the file system, allowing for persistence of user information across sessions, this is a critical part of the user management system as it allows for storing user progress and preferences in a simple file-based format
# --------------------------
def save_users(users):
    os.makedirs(os.path.dirname(USER_FILE), exist_ok=True)

    # Save user data to the JSON file, this function takes a dictionary of user data and writes it to the specified file path, ensuring that the data is properly formatted as JSON and that the necessary directories exist before attempting to write the file, this is important for maintaining the integrity of the user data and ensuring that it can be accessed and updated correctly by other parts of the application
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

# -------------------------
# USER MANAGEMENT FUNCTIONS
# Functions to retrieve user information and add new users to the data store, these functions provide the
# necessary operations to manage user accounts in the application, allowing for user registration and authentication by checking for existing users and adding new user data to the JSON file, this is a simple implementation for demonstration purposes, in a production application you would likely want to implement additional features such as password hashing, email verification, and more robust error handling for user management
# -------------------------
def get_user(username):
    users = load_users()
    return users.get(username)

# -------------------------
# ADD USER
# Adds a new user to the data store by loading existing users, adding the new user data, and saving the updated user data back to the JSON file, this function is used during the user registration process to create new user accounts, it takes a username and a dictionary of user data (which may include fields such as password, theme preference, and progress) and adds it to the existing user data before saving it back to the file system, this allows for persistence of new user accounts in the application
# -------------------------
def add_user(username, user_data):
    users = load_users()
    users[username] = user_data
    save_users(users)