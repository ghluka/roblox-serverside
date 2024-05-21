import requests


class Session:
    def __init__(self, auth_cookie:str) -> None:
        self.auth_cookie = auth_cookie
    
    def upload(self, rbxmx_path:str) -> int:
        asset_information:dict[str] = {
            "name": "MainModule",
            "description": "wassup",
            "copylocked": True,
            "groupId": ""
        }

        url:str = f"https://data.roblox.com/Data/Upload.ashx?json=1&assetid=0&type=Model&genreTypeId=1" \
            f"&name={asset_information['name']}" \
            f"&description={asset_information['description']}" \
            f"&ispublic={asset_information['copylocked']}" \
            f"&allowComments=false" \
            f"&groupId=\"\""

        session:requests.Session = requests.session()
        session.cookies.update({
           ".ROBLOSECURITY": self.auth_cookie
        })

        with open(rbxmx_path) as f:
            asset_data:str = f.read()
            f.close()

        headers = {"User-Agent": "Roblox/WinInet"}

        s = session.post(url, data=asset_data, headers=headers)
        if s.status_code == 403:
            headers["x-csrf-token"] = s.headers["x-csrf-token"]
            s = session.post(url, data=asset_data, headers=headers)
        
        try:
            return s.json()["AssetId"]
        except:
            return "Unable to upload, invalid cookie?"