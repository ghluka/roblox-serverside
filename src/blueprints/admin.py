import sqlite3
import json
from flask import Blueprint, render_template, request, session, redirect, url_for

from blueprints.auth import DB_PATH, discord_auth
from utils.inputs import PATH

admin = Blueprint("admin", __name__)

@admin.route("/admin")
@discord_auth.require_admin
def admin_home():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, discord_id, username, roblox_id, whitelist FROM users")
        users = cur.fetchall()

    return render_template("admin/admin_panel.html", users=users)


@admin.route("/admin/user/<int:user_id>", methods=["GET", "POST"])
@discord_auth.require_admin
def admin_user(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()

        if request.method == "POST":
            roblox_id = request.form.get("roblox_id")
            whitelist = request.form.get("whitelist")

            cur.execute(
                "UPDATE users SET roblox_id = ?, whitelist = ? WHERE id = ?",
                (roblox_id, whitelist, user_id),
            )
            conn.commit()

            return redirect(url_for("admin.admin_user", user_id=user_id))

        cur.execute(
            "SELECT id, discord_id, username, roblox_id, whitelist, user_data FROM users WHERE id = ?",
            (user_id,),
        )
        user = cur.fetchone()

    return render_template("admin/admin_user.html", user=user)
