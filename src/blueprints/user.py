import json
import sqlite3

import requests
from flask import Blueprint, Response, jsonify, request

from blueprints.auth import DB_PATH, discord_auth
from utils.inputs import PATH
from utils.session import Session

user = Blueprint("user", __name__)


def roblox_id_exists(roblox_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE roblox_id = ?", (roblox_id,))
        return cursor.fetchone() is not None


@user.route("/api/whitelist", methods=["GET"])
def whitelist_check():
    roblox_id = request.args.get("userid")
    game_id = request.args.get("gameid")

    with open(f"{PATH}/games/games.json", encoding="utf8") as games_file:
        games_json = json.loads(games_file.read())
    try:
        whitelist_limit = games_json[str(game_id)].get("whitelist")
    except KeyError:
        whitelist_limit = 255

    if roblox_id_exists(roblox_id):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT MAX(whitelist) FROM users WHERE roblox_id = ?", (roblox_id,)
            )
            whitelist = cursor.fetchone()[0]

            if whitelist >= whitelist_limit:
                return "true"

    return "false"


@user.route("/api/roblox_data", methods=["GET"])
@discord_auth.require_agreement
@discord_auth.require_login
def roblox_data():
    user_id = request.args.get("userid")

    session = Session(None)

    try:
        response = session.pfp_session.get(
            f"https://users.roblox.com/v1/users/{user_id}", timeout=5
        )
    except requests.exceptions.Timeout:
        return jsonify(
            {
                "error": {
                    "error": "Servers overloaded.",
                    "advice": "Please re-enter the user id in a moment!",
                }
            }
        )
    user_data = response.json()

    if user_data.get("errors"):
        return jsonify(
            {
                "error": {
                    "error": "User not found.",
                    "advice": "Please correct your User Id on the dashboard!",
                }
            }
        )

    user_data["avatarUrl"] = session.get_pfp(user_id)

    return jsonify(user_data)


@user.route("/api/decal", methods=["GET"])
@discord_auth.require_agreement
@discord_auth.require_login
def decal():
    asset = request.args.get("assetid")
    session = Session(None)
    try:
        response = session.img_session.get(
            f"https://thumbnails.roblox.com/v1/assets?assetIds={asset}&format=webp&size=30x30",
            timeout=5,
        )
    except requests.exceptions.Timeout:
        return jsonify(
            {
                "error": {
                    "error": "Servers overloaded.",
                    "advice": "Please re-enter the asset id in a moment!",
                }
            }
        )
    data = response.json()

    if data["data"][0]["state"] == "Completed":
        imgUrl = data["data"][0]["imageUrl"]
        img = session.img_session.get(imgUrl, timeout=5)
        return Response(img.content, mimetype=img.headers["Content-Type"])
    return jsonify(data)
