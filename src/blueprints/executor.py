import glob
import json
import os

from flask import Blueprint, jsonify, render_template, request

from utils.cookie import get_cookie
from utils.inputs import PATH
from utils.session import Session

executor = Blueprint("executor", __name__)

users = {}

@executor.route('/executor') 
def executor_page():
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

    return render_template("executor.html", modules=modules)

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

@executor.route('/api/ping')
def roblox_ping():
    userid = users.get(request.headers["user-id"])
    
    script = []
    if not userid:
        users.update({request.headers["user-id"]: []})
    elif len(userid) > 0:
        script = userid.copy()
        userid.clear()

    return jsonify(script)

@executor.route('/api/close', methods=['POST'])
def roblox_close():
    userid = request.headers["user-id"]

    if users.get(userid) != None:
        users.pop(userid)

    return "OK"