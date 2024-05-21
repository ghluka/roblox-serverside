import glob
import json
import os

from utils.cookie import get_cookie
from utils.inputs import PATH
from utils.session import Session

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