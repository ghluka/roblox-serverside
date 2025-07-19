import base64
import glob
import json
import os

import requests
from flask import Blueprint, render_template, request, send_file

from blueprints.auth import discord_auth
from prometheus.wrapper import obfuscate
from utils.cookie import get_cookie
from utils.inputs import PATH
from utils.session import Session

executor = Blueprint("executor", __name__)

users = {}
users_players = {}

def module_exists(module_path):
    return os.path.exists(f"{module_path}/id.txt") or os.path.exists(f"{module_path}/script.luau")

@executor.route("/api/execute", methods=["POST"])
@discord_auth.require_agreement
@discord_auth.require_login
def web_execute():
    userid = request.args.get("userid")
    script = request.data.decode("utf-8")

    with open(f"{PATH}/static/assets/lua/header.luau", encoding="utf8") as convert_file:
        header = convert_file.read()
    with open(f"{PATH}/static/assets/lua/convert.luau", encoding="utf8") as convert_file:
        convert = convert_file.read()
    with open(f"{PATH}/static/assets/lua/functions.luau", encoding="utf8") as functions_file:
        functions = functions_file.read()

    script = f"""pcall(function()
local plr = game:GetService(\"Players\"):GetPlayerByUserId({userid})
{header}
{convert}
{functions}
{script}
end)"""

    if users.get(userid) is not None:
        users[userid].append(script)
        return "OK"
    return "NO CLIENT"

@executor.route("/api/execute_ss", methods=["POST"])
@discord_auth.require_agreement
@discord_auth.require_login
def web_execute_ss():
    userid = request.args.get("userid")
    script = request.data.decode("utf-8")

    with open(f"{PATH}/static/assets/lua/functions.luau", encoding="utf8") as functions_file:
        functions = functions_file.read()

    script = f"""pcall(function()
{functions}
{script}
end)"""

    if users.get(userid) is not None:
        users[userid].append(script)
        return "OK"
    return "NO CLIENT"

@executor.route("/api/execute_module", methods=["POST"])
@discord_auth.require_agreement
@discord_auth.require_login
def web_execute_module():
    userid = request.args.get("userid")
    username = request.args.get("username")
    module_name = request.data.decode("utf-8")

    script = f"""local plr = game:GetService("Players"):GetPlayerByUserId({userid})
local target = "{username}"
"""

    module_path = f"{PATH}/modules/{module_name}"
    if module_exists(module_path):
        if os.path.exists(f"{module_path}/script.luau"):
            with open(f"{module_path}/script.luau", encoding="utf8") as script_file:
                script += script_file.read()
        elif os.path.exists(f"{module_path}/id.txt"):
            with open(f"{module_path}/id.txt", encoding="utf8") as id_file:
                module_id = id_file.read()
            with open(f"{PATH}/static/assets/lua/require.luau", encoding="utf8") as require_file:
                require_script = require_file.read()
                script += f"local m = require({module_id})\n{require_script}"

    if users.get(userid) is not None:
        users[userid].append(script)
        return "OK"
    return "NO CLIENT"

@executor.route("/api/ping", methods=["GET"])
def roblox_ping():
    userid = request.args.get("userid")
    if userid not in users:
        users[userid] = []

    user_scripts = users.get(userid, [])
    scripts_to_return = user_scripts.copy()
    user_scripts.clear()

    return scripts_to_return

@executor.route("/admin.luau", methods=["GET"])
def admin_script():
    with open(f"{PATH}/static/assets/lua/vlua.luau", encoding="utf8") as vlua_script:
        vlua_script = vlua_script.read()
    rendered = render_template("assets/lua/admin.luau", endpoint=request.headers.get("Host"), vlua=vlua_script)
    obfuscated = obfuscate(rendered) or rendered

    return send_file(obfuscated, mimetype='text/plain')

@executor.route("/api/players", methods=["GET", "POST"])
def roblox_player_ping():
    userid = request.args.get("userid")
    session = Session(None)

    if request.method == "GET":
        players = users_players.get(userid, {})
        for player in players:
            players[player]["AvatarUrl"] = session.get_pfp(players[player]["UserId"])

        return render_template("players.html", players=players)

    elif request.method == "POST":
        if users.get(userid) is not None:
            users_players[userid] = request.json
            return "OK"

    return "Connect to a server please!"

@executor.route("/api/modules", methods=["GET"])
@discord_auth.require_agreement
@discord_auth.require_login
def roblox_modules_ping():
    pinned = []
    modules = []
    auth_cookie = None
    session = None

    for module_path in glob.glob(f"{PATH}/modules/*"):
        if not module_exists(module_path) and not module_path.endswith("template"):
            with open(f"{module_path}/data.json", encoding="utf8") as data_file:
                info = json.load(data_file)

            if auth_cookie is None:
                auth_cookie = get_cookie()
                session = Session(auth_cookie)

            info["rbxmx"] = f"{module_path}/{info['rbxmx']}"
            asset_id = session.upload(info["rbxmx"], info)

            with open(f"{module_path}/id.txt", "w", encoding="utf8") as id_file:
                id_file.write(str(asset_id))

        if module_exists(module_path) and not module_path.endswith("template"):
            with open(f"{module_path}/data.json", encoding="utf8") as data_file:
                info = json.load(data_file)

            try:
                with open(f"{module_path}/{info['image']}", "rb") as image_file:
                    info["image"] = "data:image/png;base64," + base64.b64encode(image_file.read()).decode("utf-8")
            except FileNotFoundError:
                pass

            info["module"] = os.path.basename(module_path)

            (pinned if info.get("pinned") else modules).append(info)

    return render_template("modules.html", modules=[*pinned, *modules])

@executor.route("/api/close", methods=["POST"])
def roblox_close():
    userid = request.headers.get("user-id")
    users.pop(userid, None)
    users_players.pop(userid, None)
    return "OK"
