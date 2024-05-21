import requests


class Session:
    def __init__(self, auth_cookie:str) -> None:
        self.auth_cookie = auth_cookie

        self.headers = {"User-Agent": "Roblox/WinInet"}
        self.session = requests.session()
        self.session.cookies.update({
           ".ROBLOSECURITY": self.auth_cookie
        })
    
    def upload(self, rbxmx_path:str, info:dict[str]={"name": "MainModule", "description": ""}) -> int:
        info = {
            "name": info["name"],
            "description": info["description"],
            "copylocked": True,
            "groupId": ""
        }

        url = f"https://data.roblox.com/Data/Upload.ashx?json=1&assetid=0&type=Model&genreTypeId=1" \
            f"&name={info['name']}" \
            f"&description={info['description']}" \
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
            return "Unable to upload, invalid cookie?"