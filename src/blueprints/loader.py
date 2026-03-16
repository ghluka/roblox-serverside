from flask import Blueprint, Response, render_template, request

from obfuscator.wrapper import obfuscate
from utils.inputs import PATH

loader = Blueprint("loader", __name__)


@loader.route("/admin.luau", methods=["GET"])
@loader.route("/analytics.luau", methods=["GET"])
def admin_script():
    if "Roblox" not in request.headers.get("User-Agent", ""):
        with open(f"{PATH}/obfuscator/fake.luau", encoding="utf8") as fake_script:
            fake = fake_script.read() + "\n"
        return Response(fake, mimetype="text/x-lua")

    with open(f"{PATH}/obfuscator/watermark.luau", encoding="utf8") as watermark_script:
        watermark = watermark_script.read() + "\n"
    with open(f"{PATH}/static/assets/lua/vlua.luau", encoding="utf8") as vlua_script:
        vlua_script = vlua_script.read()
    rendered = render_template(
        "assets/lua/admin.luau", endpoint=request.headers.get("Host"), vlua=vlua_script
    )
    obfuscated = obfuscate(rendered)

    if obfuscated:
        with open(
            f"{PATH}/obfuscator/source.obfuscated.lua", encoding="utf8"
        ) as obfuscated_script:
            return Response(watermark + obfuscated_script.read(), mimetype="text/x-lua")
    return Response(watermark + rendered, mimetype="text/x-lua")
