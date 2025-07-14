import os
import sqlite3

from dotenv import load_dotenv
from flask import Flask, render_template, session
from markupsafe import Markup

from blueprints.auth import DB_PATH, auth, discord_auth, signup
from blueprints.executor import executor
from blueprints.user import user
from utils.cookie import get_cookie

app = Flask(__name__, static_url_path="")
app.register_blueprint(auth)
app.register_blueprint(executor)
app.register_blueprint(user)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

@app.route('/') 
def homepage():
    dashboard_button = "<a class='discord-button' href='/dashboard'><i class='bx bxl-discord-alt'></i> Log in with Discord</a>"
    if 'user' in session:
        #user = session['user']
        dashboard_button = "<a class='dashboard-button' href='/dashboard'><i class='bx bxs-dashboard'></i> Dashboard</a>"
    return render_template("index.html", dashboard_button=Markup(dashboard_button))

@app.route('/dashboard')
@discord_auth.require_login
def dashboard():
    user = session['user']
    signup(user)
    discord_id = user.get('id')
    username = user.get('username')
    avatar_id = user.get('avatar')
    avatar_url = f"https://cdn.discordapp.com/avatars/{user['id']}/{avatar_id}.png" if avatar_id else "https://cdn.discordapp.com/embed/avatars/0.png"

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, roblox_id, whitelist FROM users WHERE discord_id = ?", (discord_id,))
        result = cursor.fetchone()

    user_id, roblox_id, whitelist = 0, 1, 0
    if result:
        user_id, roblox_id, whitelist = result
    
    whitelists = {
        0: "None",
        1: "Premium"
    }
    whitelist_status = whitelists.get(whitelist, "None")

    return render_template(
        "executor.html",
        roblox_id=roblox_id, user_id=user_id, whitelist=whitelist_status,
        discord_avatar=avatar_url, discord_username=username,
    )

@app.route('/backdoor') 
def backdoor_page():

    return app.send_static_file("backdoor.html")

if __name__ == "__main__":
    get_cookie()
    app.run(debug=True)
