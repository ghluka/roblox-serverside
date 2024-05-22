import glob
import json
import os
import pathlib

from flask import Flask, render_template

PATH = pathlib.Path(__file__).parent.parent.resolve()

app = Flask(__name__, static_url_path="")

@app.route('/') 
def homepage():
    modules = []
    for module in glob.glob(f"{PATH}/modules/*"):
        if os.path.exists(f"{module}/id.txt") and not module.endswith("template"):
            with open(f"{module}/data.json") as f:
                info = json.loads(f.read())
            with open(f"{module}/id.txt") as f:
                info["id"] = f.read()

            modules.append(info)

    return render_template("index.html", modules=modules)

if __name__ == "__main__":
    app.run(debug=True)