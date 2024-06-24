import os

from flask import Blueprint, request

from utils.inputs import PATH

auth = Blueprint("auth", __name__)

@auth.route('/api/whitelist', methods=['GET'])
def authentication():
    user = request.args.get("userid")
    data = request.data.decode("utf8")
    
    if not os.path.exists(f"{PATH}/whitelisted.txt"):
        open(f"{PATH}/whitelisted.txt", "x").close()
    with open(f"{PATH}/whitelisted.txt", "r") as f:
        lines = f.readlines()
        if f"{user}\n" in lines or lines[-1] == user:
            return "true"
    return "false"