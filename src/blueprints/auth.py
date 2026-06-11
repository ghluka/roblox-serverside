import json
import os
import sqlite3
from datetime import datetime

import requests
from flask import Blueprint, jsonify, redirect, request, session, url_for

from utils.auth import DB_PATH, DiscordAuth
from utils.inputs import PATH, TOS_VERSION

auth = Blueprint("auth", __name__)

with open(f"{PATH}/CNAME", "r", encoding="utf-8") as f:
    domain = f.read().strip()

discord_auth = DiscordAuth(
    os.getenv("CLIENT_ID"),
    os.getenv("CLIENT_SECRET"),
    f"http{'s' if not (domain.startswith('localhost') or domain.startswith('127.0.0.1')) else ''}://{domain}/callback",
)


def init_db():
    """Initialize database if it doesn't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                discord_id INTEGER UNIQUE,
                email TEXT,
                username TEXT,
                roblox_id INTEGER,
                whitelist INTEGER,
                user_data TEXT,
                signup_date TEXT,
                tos_version INTEGER,
                theme TEXT DEFAULT 'violet'
            )
        """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                event_type TEXT NOT NULL,
                description TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """
        )
        try:
            conn.execute("ALTER TABLE users ADD COLUMN theme TEXT DEFAULT 'violet'")
        except sqlite3.OperationalError:
            pass
        conn.commit()


def signup(user_info):
    """Save user's data to database, if they already are a user, update it."""
    with sqlite3.connect(DB_PATH) as conn:
        discord_id = user_info["id"]
        username = user_info.get("username")
        signup_date = datetime.utcnow().isoformat()

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE discord_id = ?", (discord_id,))
        existing_user = cursor.fetchone()

        if not existing_user:
            email = user_info.get("email", "none")
            cursor.execute(
                "INSERT INTO users (discord_id, email, username, roblox_id, whitelist, user_data, signup_date, tos_version) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    discord_id,
                    email,
                    username,
                    1,
                    0,
                    json.dumps(user_info),
                    signup_date,
                    0,
                ),
            )
            new_user_id = cursor.lastrowid
            conn.commit()
        else:
            email = user_info.get("email", existing_user[2])
            cursor.execute(
                "UPDATE users SET email = ?, username = ?, user_data = ? WHERE discord_id = ?",
                (email, username, json.dumps(user_info), discord_id),
            )


@auth.route("/login")
def login():
    # return "Service under maintenance, our login system is currently offline."
    return redirect(discord_auth.get_auth_url())


@auth.route("/callback")
def callback():
    try:
        code = request.args.get("code")
        token_data = discord_auth.get_token(code)
        access_token = token_data["access_token"]
        user_info = discord_auth.fetch_user(access_token)
        session["user"] = user_info
        signup(user_info)
    except Exception:
        pass
    return redirect(url_for("dash.dashboard"))


@auth.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("homepage"))


@auth.route("/api/roblox-user-id", methods=["POST"])
@discord_auth.require_agreement
@discord_auth.require_login
def roblox_user_id():
    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify({"error": "Missing username"}), 400

    url = "https://users.roblox.com/v1/usernames/users"
    payload = {"usernames": [username], "excludeBannedUsers": False}

    try:
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        result = resp.json()
        return jsonify(result)
    except Exception:
        return jsonify(
            {
                "data": [
                    {
                        "requestedUsername": "Roblox",
                        "hasVerifiedBadge": True,
                        "id": 1,
                        "name": "Roblox",
                        "displayName": "Roblox",
                    }
                ]
            }
        )


@auth.route("/api/update_id", methods=["GET"])
@discord_auth.require_agreement
@discord_auth.require_login
def update_id():
    try:
        user = session["user"]
        discord_id = user["id"]

        with sqlite3.connect(DB_PATH) as conn:
            user_id = (
                int("".join(c for c in request.args.get("userid") if c.isdigit())) or 0
            )

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE discord_id = ?", (discord_id,))
            existing_user = cursor.fetchone()

            if existing_user:
                cursor.execute(
                    "UPDATE users SET roblox_id = ? WHERE discord_id = ?",
                    (user_id, discord_id),
                )
    except Exception:
        return "Failed!"
    return "Done!"


@auth.route("/api/agree")
@discord_auth.require_login
def agree_to_terms():
    user = session["user"]
    discord_id = user.get("id")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET tos_version = ? WHERE discord_id = ?",
            (TOS_VERSION, discord_id),
        )

    return "You have confirmed that you agree to our Terms of Service."


@auth.route("/api/theme", methods=["GET", "POST"])
@discord_auth.require_login
def user_theme():
    valid_themes = {"violet", "cyber", "ember", "ocean", "mono"}
    user = session["user"]
    discord_id = user.get("id")

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        if request.method == "POST":
            data = request.get_json(silent=True) or {}
            theme = data.get("theme")
            if theme not in valid_themes:
                return jsonify({"error": "Invalid theme"}), 400

            cursor.execute(
                "UPDATE users SET theme = ? WHERE discord_id = ?",
                (theme, discord_id),
            )
            conn.commit()
            return jsonify({"theme": theme})

        cursor.execute("SELECT theme FROM users WHERE discord_id = ?", (discord_id,))
        row = cursor.fetchone()

    theme = row[0] if row and row[0] in valid_themes else "violet"
    return jsonify({"theme": theme})


init_db()
