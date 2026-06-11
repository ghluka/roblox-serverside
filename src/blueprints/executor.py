import os
import sqlite3

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from blueprints.auth import DB_PATH, discord_auth
from utils.inputs import PATH
from utils.session import Session

executor = Blueprint("executor", __name__)

users = {}
users_players = {}


def module_exists(module_path):
    return os.path.exists(f"{module_path}/id.txt") or os.path.exists(
        f"{module_path}/script.luau"
    )


def get_current_user_roblox_id():
    """Return the roblox_id string for the currently logged-in Discord user."""
    user = session["user"]
    discord_id = user.get("id")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT roblox_id FROM users WHERE discord_id = ?", (discord_id,)
        )
        return str(cursor.fetchone()[0])


@executor.route("/api/execute", methods=["POST"])
@discord_auth.require_agreement
@discord_auth.require_login
def web_execute():
    userid = get_current_user_roblox_id()

    script = request.data.decode("utf-8")

    with open(f"{PATH}/static/assets/lua/header.luau", encoding="utf8") as convert_file:
        header = convert_file.read()
    with open(
        f"{PATH}/static/assets/lua/coregui.luau", encoding="utf8"
    ) as coregui_file:
        coregui = coregui_file.read()
    with open(
        f"{PATH}/static/assets/lua/convert.luau", encoding="utf8"
    ) as convert_file:
        convert = convert_file.read().replace("{{coreGui}}", coregui)
    with open(f"{PATH}/static/assets/lua/vlua.luau", encoding="utf8") as vlua_file:
        vluau = vlua_file.read()
    with open(
        f"{PATH}/static/assets/lua/functions.luau", encoding="utf8"
    ) as functions_file:
        functions = functions_file.read()

    script = f"""pcall(function()
local plr = game:GetService(\"Players\"):GetPlayerByUserId({userid})
{header}
{convert}
{vluau}
local function loadstring(...)
	return ls("\\n"..tostring(...).."\\n")
end
getfenv().loadstring = loadstring
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
    userid = get_current_user_roblox_id()

    script = request.data.decode("utf-8")

    with open(
        f"{PATH}/static/assets/lua/functions.luau", encoding="utf8"
    ) as functions_file:
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
    userid = get_current_user_roblox_id()

    username = request.args.get("username")
    module_name = request.data.decode("utf-8")

    script = f"""local plr = game:GetService("Players"):GetPlayerByUserId({userid})
local target = "{username}"
"""

    module_path = f"{PATH}/modules/{module_name}"
    if module_exists(module_path):
        if os.path.exists(f"{module_path}/script.luau"):
            with open(
                f"{PATH}/static/assets/lua/header.luau", encoding="utf8"
            ) as convert_file:
                header = convert_file.read()
            with open(
                f"{PATH}/static/assets/lua/coregui.luau", encoding="utf8"
            ) as coregui_file:
                coregui = coregui_file.read()
            with open(
                f"{PATH}/static/assets/lua/convert.luau", encoding="utf8"
            ) as convert_file:
                convert = convert_file.read().replace("{{coreGui}}", coregui)
            with open(
                f"{PATH}/static/assets/lua/functions.luau", encoding="utf8"
            ) as functions_file:
                functions = functions_file.read()

            with open(f"{module_path}/script.luau", encoding="utf8") as script_file:
                script = f"""pcall(function()
                local function findPlayersByUsername(partialName)
                    local players = game.Players:GetPlayers()
                    local matchingPlayers = {{}}
                    local partialNameLower = string.lower(partialName)

                    for _, player in ipairs(players) do
                        local playerNameLower = string.lower(player.Name)
                        if string.find(playerNameLower, partialNameLower) then
                            table.insert(matchingPlayers, player)
                        else
                            playerNameLower = string.lower(player.DisplayName)
                            if string.find(playerNameLower, partialNameLower) then
                                table.insert(matchingPlayers, player)
                            end
                        end
                    end

                    return matchingPlayers[1]
                end
                if \"{username}\" == \"\" then
                    local plr = game:GetService(\"Players\"):GetPlayerByUserId({userid})
                else
                    plr = findPlayersByUsername(\"{username}\")
                end
                {header}
                {convert}
                {functions}
                {script_file.read()}
                end)"""
        elif os.path.exists(f"{module_path}/id.txt"):
            with open(f"{module_path}/id.txt", encoding="utf8") as id_file:
                module_id = id_file.read()
            with open(
                f"{PATH}/static/assets/lua/require.luau", encoding="utf8"
            ) as require_file:
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


@executor.route("/api/players", methods=["GET", "POST"])
def roblox_player_ping():
    sesh = Session(None)

    if request.method == "GET":
        if "user" not in session:
            return redirect(url_for("auth.login"))

        user = session["user"]
        discord_id = user.get("id")
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT roblox_id FROM users WHERE discord_id = ?", (discord_id,)
            )
            userid = str(cursor.fetchone()[0])

        players = users_players.get(userid, {})
        for player in players:
            players[player]["AvatarUrl"] = sesh.get_pfp(players[player]["UserId"])

        return render_template("players.html", players=players)

    elif request.method == "POST":
        userid = request.args.get("userid")
        if users.get(userid) is not None:
            users_players[userid] = request.json
            return "OK"

    return "Connect to a server please!"


@executor.route("/api/players.json", methods=["GET"])
@discord_auth.require_login
def roblox_players_json():
    user = session["user"]
    discord_id = user.get("id")

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT roblox_id FROM users WHERE discord_id = ?", (discord_id,)
        )
        userid = str(cursor.fetchone()[0])

    players = users_players.get(userid, {})
    return {
        "players": [
            {
                "username": username,
                "displayName": data.get("DisplayName", username),
                "userId": data.get("UserId"),
                "avatarUrl": data.get("AvatarUrl"),
            }
            for username, data in players.items()
        ]
    }


@executor.route("/api/close", methods=["POST"])
def roblox_close():
    userid = request.headers.get("user-id")
    users.pop(userid, None)
    users_players.pop(userid, None)
    return "OK"
