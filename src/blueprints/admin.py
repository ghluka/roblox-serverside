import json
import os
import pickle
import re
import sqlite3
from datetime import datetime

from flask import (
    Blueprint,
    Response,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)

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

    modules_dir = f"{PATH}/modules"
    modules = []

    games_path = f"{PATH}/games/games.json"
    with open(games_path, encoding="utf8") as f:
        games = json.load(f)

    for name in os.listdir(modules_dir):
        if name != "template":
            module_path = os.path.join(modules_dir, name)
            json_path = os.path.join(module_path, "data.json")
            if not os.path.exists(json_path):
                continue

            with open(json_path, encoding="utf8") as f:
                data = json.load(f)

            modules.append(
                {
                    "module_name": name,
                    "name": data.get("name", name),
                    "description": data.get("description", ""),
                    "broken": data.get("broken", False),
                }
            )

    return render_template(
        "admin/panel.html", games=games, users=users, modules=modules
    )


@admin.route("/admin/user/<int:user_id>", methods=["GET", "POST"])
@discord_auth.require_admin
def admin_user(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()

        if request.method == "POST":
            roblox_id = request.form.get("roblox_id")
            whitelist = request.form.get("whitelist")

            cur.execute("SELECT whitelist FROM users WHERE id = ?", (user_id,))
            old_row = cur.fetchone()
            old_whitelist = old_row[0] if old_row else None

            cur.execute(
                "UPDATE users SET roblox_id = ?, whitelist = ? WHERE id = ?",
                (roblox_id, whitelist, user_id),
            )
            conn.commit()

            if old_whitelist is not None and str(old_whitelist) != str(whitelist):
                with open(f"{PATH}/ranks.json", "r", encoding="utf8") as f:
                    ranks = json.load(f)
                old_name = ranks.get(str(old_whitelist), str(old_whitelist))
                new_name = ranks.get(str(whitelist), str(whitelist))
                timestamp = datetime.utcnow().isoformat()
                cur.execute(
                    "INSERT INTO user_history (user_id, event_type, description, timestamp) VALUES (?, ?, ?, ?)",
                    (user_id, "whitelist", f"Whitelist tier changed from {old_name} to {new_name}", timestamp),
                )
                conn.commit()

            return redirect(url_for("admin.admin_user", user_id=user_id))

        cur.execute(
            "SELECT id, discord_id, username, roblox_id, whitelist, user_data FROM users WHERE id = ?",
            (user_id,),
        )
        user = cur.fetchone()

    return render_template("admin/edit/user.html", user=user)


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


@admin.route("/admin/review/reject/", defaults={"placeid": ""}, methods=["POST"])
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


@admin.route("/admin/module/<module_name>", methods=["GET", "POST"])
@discord_auth.require_admin
def admin_module_edit(module_name):
    module_path = f"{PATH}/modules/{module_name}"
    json_path = f"{module_path}/data.json"

    if not os.path.exists(json_path):
        return "Not found", 404

    module_id = 0
    if os.path.exists(f"{module_path}/id.txt"):
        try:
            with open(f"{module_path}/id.txt", "r") as f:
                module_id = int(f.read().strip() or 0)
        except:
            module_id = 0

    if request.method == "POST":
        with open(json_path, encoding="utf8") as f:
            data = json.load(f)

        data["name"] = request.form.get("name")
        data["description"] = request.form.get("description")
        data["controls"] = request.form.get("controls") or None
        if data["controls"] == "None":
            data["controls"] = None
        data["roblox_name"] = request.form.get("roblox_name")
        data["roblox_description"] = request.form.get("roblox_description")
        data["broken"] = bool(request.form.get("broken", False))
        data["badges"] = [
            b.strip() for b in request.form.get("badges", "").split(",") if b.strip()
        ]

        with open(json_path, "w", encoding="utf8") as f:
            json.dump(data, f, indent=4)

        return redirect(f"/admin/module/{module_name}")

    with open(json_path, encoding="utf8") as f:
        data = json.load(f)

    has_script = os.path.exists(f"{module_path}/script.luau")
    has_rbxmx = os.path.exists(f"{module_path}/{data.get('rbxmx','')}")

    return render_template(
        "admin/edit/module.html",
        module=data,
        module_name=module_name,
        has_script=has_script,
        has_rbxmx=has_rbxmx,
        module_id=module_id,
    )


@admin.route("/admin/module/<module_name>/upload_rbxmx", methods=["POST"])
@discord_auth.require_admin
def admin_upload_rbxmx(module_name):
    module_path = f"{PATH}/modules/{module_name}"

    file = request.files.get("file")
    if not file or not file.filename.endswith(".rbxmx"):
        return "Invalid", 400

    luau = f"{module_path}/script.luau"
    if os.path.exists(luau):
        os.remove(luau)

    save_path = os.path.join(module_path, file.filename)
    file.save(save_path)

    json_path = f"{module_path}/data.json"
    with open(json_path, encoding="utf8") as f:
        data = json.load(f)
    data["rbxmx"] = file.filename
    with open(json_path, "w", encoding="utf8") as f:
        json.dump(data, f, indent=4)

    return redirect(f"/admin/module/{module_name}")


@admin.route("/admin/module/<module_name>/script.luau")
@discord_auth.require_admin
def admin_view_script(module_name):
    if "/" in module_name or "\\" in module_name or ".." in module_name:
        return Response('print("Hello World!")', mimetype="text/x-lua")

    path = os.path.join(f"{PATH}/modules/", module_name, "script.luau")

    if not os.path.isfile(path):
        return Response('print("Hello World!")', mimetype="text/x-lua")

    return send_file(path, mimetype="text/x-lua")


@admin.route("/admin/module/<module_name>/save_script", methods=["POST"])
@discord_auth.require_admin
def admin_save_script(module_name):
    module_path = f"{PATH}/modules/{module_name}"

    content = request.form.get("content", "").replace("\r\n", "\n")
    with open(f"{module_path}/script.luau", "w", encoding="utf8") as f:
        f.write(content)

    json_path = f"{module_path}/data.json"
    with open(json_path, encoding="utf8") as f:
        data = json.load(f)
    if data.get("rbxmx"):
        rbx = f"{module_path}/{data['rbxmx']}"
        if os.path.exists(rbx):
            os.remove(rbx)
        data["rbxmx"] = None
    with open(json_path, "w", encoding="utf8") as f:
        json.dump(data, f, indent=4)

    return "OK"


@admin.route("/admin/module/<module_name>/upload_image", methods=["POST"])
@discord_auth.require_admin
def admin_upload_image(module_name):
    module_path = f"{PATH}/modules/{module_name}"
    os.makedirs(module_path, exist_ok=True)

    file = request.files.get("image")
    if not file:
        return "No file uploaded", 400

    image_path = f"{module_path}/image.png"
    file.save(image_path)

    return "OK"


@admin.route("/admin/module/<module_name>/switch_to_script", methods=["POST"])
@discord_auth.require_admin
def admin_switch_to_script(module_name):
    module_path = f"{PATH}/modules/{module_name}"
    json_path = f"{module_path}/data.json"

    with open(json_path, encoding="utf8") as f:
        data = json.load(f)

    rbxmx = data.get("rbxmx")
    if not rbxmx:
        return "No RBXMX to convert", 400

    rbx_path = os.path.join(module_path, rbxmx)
    if os.path.exists(rbx_path):
        os.remove(rbx_path)

    data["rbxmx"] = None

    script_path = os.path.join(module_path, "script.luau")
    if not os.path.exists(script_path):
        with open(script_path, "w", encoding="utf8") as f:
            f.write("print(`Hello world!` :: string)")

    with open(json_path, "w", encoding="utf8") as f:
        json.dump(data, f, indent=4)

    return redirect(f"/admin/module/{module_name}")


@admin.route("/admin/create_module", methods=["POST"])
@discord_auth.require_admin
def admin_create_module():
    data = request.get_json()
    module_name = data.get("name", "").strip()
    module_path = f"{PATH}/modules/{module_name}"

    if not module_name:
        return jsonify({"success": False, "error": "Module name is required"})

    if not re.match(r"^[A-Za-z0-9_-]+$", module_name):
        return jsonify({"success": False, "error": "Invalid module name"})

    if os.path.exists(module_path):
        return jsonify({"success": False, "error": "Module already exists"})

    os.makedirs(module_path)

    json_path = os.path.join(module_path, "data.json")
    default_json = {
        "roblox_name": "MainModule",
        "roblox_description": "Test module",
        "name": module_name,
        "description": "Description",
        "rbxmx": "MainModule.rbxmx",
    }
    with open(json_path, "w") as f:
        json.dump(default_json, f, indent=4)

    script_path = os.path.join(module_path, "script.luau")
    with open(script_path, "w") as f:
        f.write(f"print(`Hello world!` :: string)")
    return jsonify({"success": True})


@admin.route("/admin/module/<module_name>/delete", methods=["POST"])
@discord_auth.require_admin
def admin_delete_module(module_name):
    module_path = f"{PATH}/modules/{module_name}"

    if not os.path.exists(module_path):
        return jsonify({"success": False, "error": "Module does not exist"}), 404

    if module_name.lower() == "template":
        return jsonify({"success": False, "error": "Cannot delete template"}), 400

    try:
        for entry in os.listdir(module_path):
            file_path = os.path.join(module_path, entry)
            if os.path.isfile(file_path):
                os.remove(file_path)
            else:
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": f"Directory inside module not allowed: {entry}",
                        }
                    ),
                    400,
                )

        os.rmdir(module_path)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

    return jsonify({"success": True})


@admin.route("/admin/module/<module_name>/save_id", methods=["POST"])
@discord_auth.require_admin
def admin_save_id(module_name):
    module_path = f"{PATH}/modules/{module_name}"
    id_path = os.path.join(module_path, "id.txt")

    new_id = request.form.get("id_value", "").strip()

    if new_id == "":
        try:
            if os.path.isfile(id_path):
                os.remove(id_path)
        except:
            return (
                jsonify({"success": False, "error": "Failed to remove ID, try again."}),
                500,
            )
        return jsonify({"success": True})
    if not new_id.isdigit():
        return jsonify({"success": False, "error": "ID must be numeric"}), 400

    try:
        with open(id_path, "w") as f:
            f.write(new_id)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

    return jsonify({"success": True})


@admin.route("/admin/game/<placeid>", methods=["GET", "POST"])
@discord_auth.require_admin
def admin_game_edit(placeid):
    games_path = f"{PATH}/games/games.json"

    with open(games_path, encoding="utf8") as f:
        games = json.load(f)

    if placeid not in games:
        return "Game not found", 404

    if request.method == "POST":
        whitelist = request.form.get("whitelist")

        games[placeid]["url"] = f"https://www.roblox.com/games/{placeid}"
        games[placeid]["whitelist"] = int(whitelist)

        with open(games_path, "w", encoding="utf8") as f:
            json.dump(games, f, indent=4)

        return redirect(f"/admin/game/{placeid}")

    game = games[placeid]

    return render_template("admin/edit/game.html", game=game, placeid=placeid)


@admin.route("/admin/set_cookie", methods=["POST"])
@discord_auth.require_admin
def admin_set_cookie():
    cookie = request.get_data(as_text=True)
    cookie_path = f"{PATH}/cookie.pkl"
    with open(cookie_path, "wb") as file:
        pickle.dump(cookie, file)

    return jsonify({"success": True})
