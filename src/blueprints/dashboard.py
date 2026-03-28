import json
import sqlite3

from flask import Blueprint, render_template, session

from blueprints.auth import DB_PATH, discord_auth, signup
from utils.inputs import PATH, TOS_VERSION

dash = Blueprint("dash", __name__)


@dash.route("/dashboard")
@discord_auth.require_login
def dashboard():
    user = session["user"]
    signup(user)

    discord_id = user.get("id")
    username = user.get("username")
    avatar_id = user.get("avatar")
    avatar_url = (
        f"https://cdn.discordapp.com/avatars/{user['id']}/{avatar_id}."
        f"{'gif' if avatar_id.startswith('a_') else 'png'}"
        if avatar_id
        else "https://cdn.discordapp.com/embed/avatars/0.png"
    )

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, roblox_id, whitelist, tos_version FROM users WHERE discord_id = ?",
            (discord_id,),
        )
        result = cursor.fetchone()

    user_id, roblox_id, whitelist, tos_db_version = 0, 1, 0, 0
    if result:
        user_id, roblox_id, whitelist, tos_db_version = result

    with open(f"{PATH}/ranks.json", "r", encoding="utf8") as f:
        whitelists = json.loads(f.read())
    whitelist_status = whitelists.get(str(whitelist), "None")

    new_user = tos_db_version == 0
    tos_updated = not new_user and tos_db_version != TOS_VERSION

    return render_template(
        "executor.html",
        roblox_id=roblox_id,
        user_id=user_id,
        whitelist_status=whitelist_status,
        whitelist=whitelist,
        discord_avatar=avatar_url,
        discord_username=username,
        tos_updated=tos_updated,
        new_user=new_user,
    )
