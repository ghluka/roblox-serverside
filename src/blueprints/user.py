import os

import requests
import requests_cache
from flask import Blueprint, jsonify, request

from utils.inputs import PATH
from utils.session import Session

user = Blueprint("user", __name__)

@user.route('/api/whitelist', methods=['GET'])
def whitelist_check():
    user_id = request.args.get("userid")

    whitelist_path = f"{PATH}/whitelisted.txt"
    if not os.path.exists(whitelist_path):
        with open(whitelist_path, "x", encoding="utf8"):
            pass

    with open(whitelist_path, "r", encoding="utf8") as file:
        lines = file.readlines()
        if f"{user_id}\n" in lines or (lines and lines[-1].strip() == user_id):
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
