import sqlite3
import os
import json
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify

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


@admin.route("/admin/review")
@discord_auth.require_admin
def admin_review():
    with open(f"{PATH}/games/review.json", encoding="utf8") as f:
        review = json.load(f)

    return jsonify(review)


@admin.route("/admin/review/approve/<placeid>", methods=["POST"])
@discord_auth.require_admin
def admin_review_approve(placeid):
    review_path = f"{PATH}/games/review.json"
    games_path = f"{PATH}/games/games.json"

    with open(review_path, encoding="utf8") as f:
        review = json.load(f)

    if placeid not in review:
        return "", 404

    with open(games_path, encoding="utf8") as f:
        games = json.load(f)

    whitelist = int(request.form.get("whitelist", 0))

    games[placeid] = {
        "placeid": int(placeid),
        "url": review[placeid]["url"],
        "whitelist": whitelist,
    }

    with open(games_path, "w", encoding="utf8") as f:
        json.dump(games, f, indent=4)

    del review[placeid]
    with open(review_path, "w", encoding="utf8") as f:
        json.dump(review, f, indent=4)

    return "OK"


@admin.route("/admin/review/reject/<placeid>", methods=["POST"])
@discord_auth.require_admin
def admin_review_reject(placeid):
    review_path = f"{PATH}/games/review.json"

    with open(review_path, encoding="utf8") as f:
        review = json.load(f)

    if placeid not in review:
        return "", 404

    del review[placeid]

    with open(review_path, "w", encoding="utf8") as f:
        json.dump(review, f, indent=4)

    return "OK"