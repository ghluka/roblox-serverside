import os
import sqlite3
from datetime import datetime

from flask import Blueprint, redirect, request, session, url_for

from utils.auth import DiscordAuth

auth = Blueprint("auth", __name__)

discord_auth = DiscordAuth(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"), "https://nett.wtf/callback")

DB_PATH = "users.db"

def init_db():
    """Initialize database if it doesn't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                discord_id INTEGER UNIQUE,
                email TEXT,
                username TEXT,
                roblox_id INTEGER,
                whitelist INTEGER,
                signup_date TEXT
            )
        """)
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
                "INSERT INTO users (discord_id, email, username, roblox_id, whitelist, signup_date) VALUES (?, ?, ?, ?, ?, ?)",
                (discord_id, email, username, 1, 0, signup_date)
            )
            conn.commit()
        else:
            email = user_info.get("email", existing_user[2])
            cursor.execute(
                "UPDATE users SET email = ?, username = ? WHERE discord_id = ?",
                (email, username, discord_id)
            )

@auth.route("/login")
def login():
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
    except:
        pass
    return redirect(url_for("dash.dashboard"))

@auth.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("homepage"))

@auth.route("/api/update_id", methods=["GET"])
def update_id():
    try:
        user = session["user"]
        discord_id = user["id"]

        with sqlite3.connect(DB_PATH) as conn:
            user_id = int("".join(c for c in request.args.get("userid") if c.isdigit())) or 0

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE discord_id = ?", (discord_id,))
            existing_user = cursor.fetchone()

            if existing_user:
                cursor.execute(
                    "UPDATE users SET roblox_id = ? WHERE discord_id = ?",
                    (user_id, discord_id)
                )
    except:
        pass
    return "Done!"

init_db()
