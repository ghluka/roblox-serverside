import requests


class Session:
    def __init__(self, auth_cookie:str) -> None:
        self.auth_cookie = auth_cookie

        self.headers = {"User-Agent": "Roblox/WinInet"}
        self.session = requests.session()
        self.session.cookies.update({
           ".ROBLOSECURITY": self.auth_cookie
        })
    
    def upload(self, rbxmx_path:str, info:dict[str]={"roblox_name": "MainModule", "roblox_description": ""}) -> int:
        info = {
            "roblox_name": info["roblox_name"],
            "roblox_description": info["roblox_description"],
            "copylocked": True,
            "groupId": ""
        }

        url = f"https://data.roblox.com/Data/Upload.ashx?json=1&assetid=0&type=Model&genreTypeId=1" \
            f"&name={info['roblox_name']}" \
            f"&description={info['roblox_description']}" \
            f"&ispublic={info['copylocked']}" \
            f"&allowComments=false" \
            f"&groupId=\"\""

        with open(rbxmx_path) as f:
            rbxmx = f.read()
            f.close()

        s = self.session.post(url, data=rbxmx, headers=self.headers)
        if s.status_code == 403:
            self.headers["x-csrf-token"] = s.headers["x-csrf-token"]
            s = self.session.post(url, data=rbxmx, headers=self.headers)
        
        try:
            return s.json()["AssetId"]
        except:
            try:
                return s.text
            except:
                return "Unable to upload, invalid cookie?"