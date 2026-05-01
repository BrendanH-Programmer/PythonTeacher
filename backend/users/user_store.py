import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
USER_FILE = os.path.join(BASE_DIR, "data", "users.json")

def load_users():
    if not os.path.exists(USER_FILE):
        return {}

    with open(USER_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_users(users):
    os.makedirs(os.path.dirname(USER_FILE), exist_ok=True)

    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)


def get_user(username):
    users = load_users()
    return users.get(username)


def add_user(username, user_data):
    users = load_users()
    users[username] = user_data
    save_users(users)