from datetime import timedelta

import requests
import requests_cache


class Session:
    def __init__(self, auth_cookie: str) -> None:
        """Initializes a session with a Roblox authentication cookie."""
        self.auth_cookie = auth_cookie
        self.headers = {"User-Agent": "Roblox/WinInet"}
        self.session = requests.session()
        self.pfp_session = requests_cache.CachedSession(
            "roblox_userdata", expire_after=timedelta(hours=1)
        )
        self.img_session = requests_cache.CachedSession(
            "roblox_imgdata", expire_after=timedelta(days=1)
        )
        self.session.cookies.update({".ROBLOSECURITY": self.auth_cookie})

    def get_pfp(self, user_id: str) -> str:
        """Fetches the avatar headshot URL for the given user ID."""
        url = (
            "https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds="
            f"{user_id}&size=420x420&format=Png&isCircular=false&thumbnailType=HeadShot"
        )
        default = (
            "data:image/svg+xml;base64,"
            "PHN2ZyB2ZXJzaW9uPSIxLjEiIGlkPSJMYXllcl8xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHg9IjAiIHk9IjAiIHdpZHRoPSI5MCIgaGVpZ2h0PSI5MCIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSI+PHN0eWxlPi5zdDJ7ZmlsbDpub25lO3N0cm9rZTojMDAwO3N0cm9rZS13aWR0aDoyO3N0cm9rZS1saW5lY2FwOnJvdW5kO3N0cm9rZS1saW5lam9pbjpyb3VuZDtzdHJva2UtbWl0ZXJsaW1pdDoxMH08L3N0eWxlPjxnIGlkPSJ1bmFwcHJvdmVkXzFfIj48cGF0aCBpZD0iYmdfMl8iIGZpbGw9IiM2NTY2NjgiIGQ9Ik0wIDBoOTB2OTBIMHoiLz48ZyBpZD0idW5hcHByb3ZlZCIgb3BhY2l0eT0iLjMiPjxjaXJjbGUgY2xhc3M9InN0MiIgY3g9IjQ1IiBjeT0iNDguOCIgcj0iMTAiLz48cGF0aCBjbGFzcz0ic3QyIiBkPSJNMzggNDEuN2wxNCAxNC4xTTMyLjUgMjMuNWgtNHY0TTI4LjUgNjIuNXY0aDRNMjguNSAzMS44djZNMjguNSA0MnY2TTI4LjUgNTIuMnY2TTU3LjUgNjYuNWg0di00TTYxLjUgNTguMnYtNk02MS41IDQ4di02TTYxLjUgMzcuOHYtNE0zNi44IDY2LjVoNk00Ny4yIDY2LjVoNk0zNi44IDIzLjVoNk00Ny4yIDIzLjVoNE01MS40IDIzLjZsMy41IDMuNU01Ny45IDMwLjFsMy41IDMuNU01MS4yIDIzLjh2M001OC41IDMzLjhoM001MS4yIDMwLjJ2My42aDMuNiIvPjwvZz48L2c+PC9zdmc+"
        )

        try:
            response = self.pfp_session.get(url, timeout=5).json()
        except requests.exceptions.Timeout:
            return default

        if response.get("data") and response["data"][0]["state"] == "Completed":
            return response["data"][0]["imageUrl"]

        return default

    def upload(self, rbxmx_path: str, info: dict[str, str] = None) -> int:
        """Uploads a Roblox XML model file and returns the asset ID."""
        if info is None:
            info = {"roblox_name": "MainModule", "roblox_description": ""}

        url = (
            "https://data.roblox.com/Data/Upload.ashx?json=1&assetid=0&type=Model&genreTypeId=1"
            f"&name={info['roblox_name']}"
            f"&description={info['roblox_description']}"
            "&ispublic=True"
            "&allowComments=false"
            "&groupId="
        )

        with open(rbxmx_path, "r", encoding="utf8") as file:
            rbxmx = file.read()

        response = self.session.post(url, data=rbxmx, headers=self.headers)

        if response.status_code == 403:
            self.headers["x-csrf-token"] = response.headers.get("x-csrf-token", "")
            response = self.session.post(url, data=rbxmx, headers=self.headers)

        try:
            return response.json()
        except (ValueError, KeyError):
            return "Unable to upload, invalid cookie?"
