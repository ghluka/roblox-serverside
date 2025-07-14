import os
import sqlite3

import requests
import requests_cache
from flask import Blueprint, jsonify, request

from blueprints.auth import DB_PATH
from utils.inputs import PATH
from utils.session import Session

user = Blueprint("user", __name__)

def roblox_id_exists(roblox_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE roblox_id = ?", (roblox_id,))
        return cursor.fetchone() is not None

@user.route('/api/whitelist', methods=['GET'])
def whitelist_check():
    roblox_id = request.args.get("userid")
    game_id = request.args.get("gameid")

    if roblox_id_exists(roblox_id):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT whitelist FROM users WHERE roblox_id = ?", (roblox_id,))
            whitelist = cursor.fetchone()[0]
            
            if whitelist > 0:
                return "true"

    return "false"

@user.route('/api/roblox_data', methods=['GET'])
def roblox_data():
    user_id = request.args.get("userid")

    session = Session(None)

    try:
        response = session.pfp_session.get(f"https://users.roblox.com/v1/users/{user_id}", timeout=5)
    except requests.exceptions.Timeout:
        return jsonify({
            "error": {
                "error": "Servers overloaded.",
                "advice": "Please re-enter the user id in a moment!"
            }
        })
    user_data = response.json()

    if user_data.get("errors"):
        return jsonify({
            "error": {
                "error": "User not found.",
                "advice": "Please correct your User Id on the dashboard!"
            }
        })

    user_data["avatarUrl"] = session.get_pfp(user_id)

    return jsonify(user_data)
