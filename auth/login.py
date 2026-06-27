import json
import os

USERS_FILE = "auth/users.json"


def load_users():

    if not os.path.exists(USERS_FILE):
        return []

    with open(USERS_FILE, "r") as file:
        return json.load(file)


def save_users(users):

    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)


def register_user(email, password):

    users = load_users()

    for user in users:

        if user["email"] == email:
            return False

    users.append({
        "email": email,
        "password": password
    })

    save_users(users)

    return True


def login_user(email, password):

    users = load_users()

    for user in users:

        if (
            user["email"] == email
            and
            user["password"] == password
        ):
            return True

    return False