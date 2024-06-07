import glob
import json
import os

from flask import Flask, render_template

from blueprints.executor import executor
from utils.cookie import get_cookie
from utils.inputs import PATH
from utils.session import Session

app = Flask(__name__, static_url_path="")
app.register_blueprint(executor)

modules = []
for module in glob.glob(f"{PATH}/modules/*"):
    if os.path.exists(f"{module}/id.txt") and not module.endswith("template"):
        with open(f"{module}/data.json") as f:
            info = json.loads(f.read())
        with open(f"{module}/id.txt") as f:
            info["id"] = f.read()
        if os.path.exists(f"{module}/script.lua"):
            with open(f"{module}/script.lua") as f:
                info["script"] = f.read()
        else:
            info["script"] = f"require({info['id']})(username)"
        
        modules.append(info)

@app.route('/') 
def homepage():
    return app.send_static_file("index.html")

@app.route('/executor') 
def executor():
    return render_template("executor.html", modules=modules)

if __name__ == "__main__":
    auth_cookie = get_cookie()

    for module in glob.glob(f"{PATH}/modules/*"):
        if not os.path.exists(f"{module}/id.txt"):
            s = Session(auth_cookie)

            with open(f"{module}/data.json") as f:
                info = json.loads(f.read())
            info["rbxmx"] = f"{module}/{info['rbxmx']}"

            asset_id = s.upload(info["rbxmx"], info)

            with open(f"{module}/id.txt", "w+") as f:
                f.write(str(asset_id))

    app.run(debug=True)