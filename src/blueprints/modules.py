import base64
import glob
import json
import os

import requests
from flask import Blueprint, abort, render_template, request, send_file

from blueprints.auth import discord_auth
from utils.cookie import get_cookie
from utils.inputs import PATH
from utils.session import Session

scripthub = Blueprint("modules", __name__)


def module_exists(module_path):
    return os.path.exists(f"{module_path}/id.txt") or os.path.exists(
        f"{module_path}/script.luau"
    )


@scripthub.route("/api/module/<module_name>.png")
@discord_auth.require_agreement
@discord_auth.require_login
def module_image(module_name):
    if not module_exists(f"{PATH}/modules/{module_name}"):
        abort(404)

    with open(f"{PATH}/modules/{module_name}/data.json", encoding="utf8") as data_file:
        info = json.load(data_file)

    try:
        with open(f"{PATH}/modules/{module_name}/{info['image']}", "rb") as _:
            return send_file(
                f"{PATH}/modules/{module_name}/{info['image']}", mimetype="image/png"
            )
    except FileNotFoundError:
        abort(404)


@scripthub.route("/api/modules", methods=["GET"])
@discord_auth.require_agreement
@discord_auth.require_login
def roblox_modules():
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

            try:
                info["rbxmx"] = f"{module_path}/{info['rbxmx']}"
                asset_id = session.upload(info["rbxmx"], info)

                with open(f"{module_path}/id.txt", "w", encoding="utf8") as id_file:
                    id_file.write(str(asset_id))
            except FileNotFoundError:
                pass

        if module_exists(module_path) and not module_path.endswith("template"):
            with open(f"{module_path}/data.json", encoding="utf8") as data_file:
                info = json.load(data_file)

            info["module"] = os.path.basename(module_path)
            info["image"] = f"/api/module/{info['module']}.png"

            (pinned if info.get("pinned") else modules).append(info)

    return render_template("modules.html", modules=[*pinned, *modules])
