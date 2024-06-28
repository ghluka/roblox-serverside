import glob
import json
import os

from flask import Blueprint, render_template, request
import requests

from utils.cookie import get_cookie
from utils.inputs import PATH
from utils.session import Session

executor = Blueprint("executor", __name__)

users = {}
users_players = {}

@executor.route('/api/execute', methods=['POST'])
def web_execute():
    userid = request.args.get("userid")
    script = request.data.decode("utf8")
    
    if users.get(userid) != None:
        users[userid].append(script)
        return "OK"
    return "NO CLIENT"

@executor.route('/api/execute_module', methods=['POST'])
def web_execute_module():
    userid = request.args.get("userid")
    user = request.args.get("username")
    data = request.data.decode("utf8")
    script = f"local username = \"{user}\"\n"

    module = f"{PATH}/modules/{data}"
    if os.path.exists(module):
        if os.path.exists(f"{module}/script.lua"):
            with open(f"{module}/script.lua") as f:
                script += f.read()
        elif os.path.exists(f"{module}/id.txt"):
            with open(f"{module}/id.txt") as f:
                script += f"require({f.read()})(username)"
    
    if users.get(userid) != None:
        users[userid].append(script)
        return "OK"
    return "NO CLIENT"

@executor.route('/api/ping', methods=['GET'])
def roblox_ping():
    userid = request.args.get("userid")
    user = users.get(userid)
    
    script = []
    if not userid in users:
        users[userid] = []
    elif len(userid) > 0:
        script = user.copy()
        user.clear()
    
    return script

@executor.route('/api/players', methods=['GET', 'POST'])
def roblox_player_ping():
    userid = request.args.get("userid")
    if request.method == 'GET':
        if users_players.get(userid):
            players = users_players[userid]

            for player in players:
                avatar = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={userid}&size=420x420&format=Png&isCircular=false&thumbnailType=HeadShot").json()
                if avatar["data"][0]["state"] == "Completed":
                    players[player]["AvatarUrl"] = avatar["data"][0]["imageUrl"]

            return render_template("players.html", players=players)
        
    elif request.method == 'POST':
        if not users.get(userid):
            players = request.json
            users_players[userid] = players
            return "OK"
        
    return "Connect to a server please!"

@executor.route('/api/modules', methods=['GET'])
def roblox_modules_ping():
    pinned = []
    modules = []

    auth_cookie = None
    s = None

    for module in glob.glob(f"{PATH}/modules/*"):
        if not os.path.exists(f"{module}/id.txt") and not module.endswith("template"):
            if auth_cookie == None:
                auth_cookie = get_cookie()
                s = Session(auth_cookie)
            with open(f"{module}/data.json") as f:
                info = json.loads(f.read())
            info["rbxmx"] = f"{module}/{info['rbxmx']}"

            asset_id = s.upload(info["rbxmx"], info)
            
            with open(f"{module}/id.txt", "w+") as f:
                f.write(str(asset_id))
        if os.path.exists(f"{module}/id.txt") and not module.endswith("template"):
            with open(f"{module}/data.json") as f:
                info = json.loads(f.read())
            with open(f"{module}/id.txt") as f:
                info["id"] = f.read()
                
            info["module"] = module.replace('\\', '/').split('/')[-1]

            if info.get("pinned"):
                pinned.append(info)
            else:
                modules.append(info)
    
    modules = [*pinned, *modules]
    return render_template("modules.html", modules=modules)

@executor.route('/api/close', methods=['POST'])
def roblox_close():
    userid = request.headers["user-id"]

    if users.get(userid) != None:
        users.pop(userid)
    if users_players.get(userid) != None:
        users_players.pop(userid)

    return "OK"