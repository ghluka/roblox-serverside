import os
import sqlite3
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv
from flask import redirect, session, url_for

from utils.inputs import PATH

DB_PATH = "users.db"


class DiscordAuth:
    def __init__(self, client_id, client_secret, redirect_uri, scope="identify email"):
        """Initialize with Discord application credentials."""
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope

        self.auth_base = "https://discord.com/api/oauth2"
        self.user_info_url = "https://discord.com/api/users/@me"

    def get_auth_url(self):
        """Generate the Discord OAuth2 login URL."""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": self.scope,
        }
        if dev_auth():
            return self.redirect_uri
        return f"{self.auth_base}/authorize?{urlencode(params)}"

    def get_token(self, code):
        """Exchange the authorization code for an access token."""
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        if dev_auth():
            return {"access_token": "dev_auth()"}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return requests.post(
            f"{self.auth_base}/token", data=payload, headers=headers, timeout=5
        ).json()

    def fetch_user(self, access_token):
        """Fetch the user info using the access token."""
        if dev_auth():
            return {
                "id": "1081004946872352958",
                "username": "Clyde",
                "avatar": "a_6170487d32fdfe9f988720ad80e6ab8c",
            }
        headers = {"Authorization": f"Bearer {access_token}"}
        return requests.get(self.user_info_url, headers=headers, timeout=5).json()

    def require_login(self, func):
        """Decorator to protect routes that require login."""

        def wrapped(*args, **kwargs):
            if "user" not in session:
                return redirect(url_for("auth.login"))
            if (
                not dev_auth()
                and session["user"].get("id", "1") == "1081004946872352958"
            ):
                return redirect(url_for("auth.logout"))
            return func(*args, **kwargs)

        wrapped.__name__ = func.__name__
        return wrapped

    def require_agreement(self, func):
        """Decorator to protect routes that require a Terms of Service agreement."""

        def wrapped(*args, **kwargs):
            if "user" not in session:
                return redirect(url_for("auth.login"))

            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT tos_version FROM users WHERE discord_id = ?",
                    (session.get("user").get("id"),),
                )
                result = cursor.fetchone()[0]

                with open(f"{PATH}/static/terms.html", "r", encoding="utf8") as f:
                    version = int(f.read().split('version="')[1].split('"')[0])

                if result == 0 or result != version:
                    return ""

            return func(*args, **kwargs)

        wrapped.__name__ = func.__name__
        return wrapped

    def require_admin(self, func):
        """Decorator to protect routes that require an administrator rank."""

        def wrapped(*args, **kwargs):
            if "user" not in session:
                return redirect("/404.html")

            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT whitelist FROM users WHERE discord_id = ?",
                    (session.get("user").get("id"),),
                )
                result = cursor.fetchone()[0]

                if result < 255:
                    return redirect("/404.html")

            return func(*args, **kwargs)

        wrapped.__name__ = func.__name__
        return wrapped


def dev_auth() -> bool:
    """Returns whether or not dev_auth is enabled."""
    load_dotenv(override=True)
    auth_str = os.getenv("DEV_AUTH", "faux").strip().lower()
    if auth_str == "true":
        return True
    return False
