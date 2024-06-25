import os

import requests
from flask import Blueprint, jsonify, request

from utils.inputs import PATH

user = Blueprint("user", __name__)

@user.route('/api/whitelist', methods=['GET'])
def whitelist_check():
    user_id = request.args.get("userid")
    data = request.data.decode("utf8")
    
    if not os.path.exists(f"{PATH}/whitelisted.txt"):
        open(f"{PATH}/whitelisted.txt", "x").close()
    with open(f"{PATH}/whitelisted.txt", "r") as f:
        lines = f.readlines()
        if f"{user_id}\n" in lines or lines[-1] == user_id:
            return "true"
    return "false"

@user.route('/api/roblox_data', methods=['GET'])
def roblox_data():
    user_id = request.args.get("userid")
    data = request.data.decode("utf8")
    
    user_data = requests.get(f"https://users.roblox.com/v1/users/{user_id}").json()

    if user_data.get("errors"):
        return jsonify({"error":{
            "error":"User not found.",
            "advice":"Please correct your User Id on the dashboard!"
        }})
    
    avatar = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=420x420&format=Png&isCircular=false&thumbnailType=HeadShot").json()
    if avatar["data"][0]["state"] == "Completed":
        user_data["avatarUrl"] = avatar["data"][0]["imageUrl"]

    return jsonify(user_data)