import os
import sqlite3

from dotenv import load_dotenv
from flask import Flask, render_template, session

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
    return app.send_static_file("index.html")

@app.route('/dashboard')
@discord_auth.require_login
def dashboard():
    user = session['user']
    signup(user)
    discord_id = user.get('id')
    avatar_id = user.get('avatar')
    avatar_url = f"https://cdn.discordapp.com/avatars/{user['id']}/{avatar_id}.png" if avatar_id else "https://cdn.discordapp.com/embed/avatars/0.png"

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT roblox_id, whitelist FROM users WHERE discord_id = ?", (discord_id,))
        result = cursor.fetchone()

    roblox_id, whitelist = 1, 0
    if result:
        roblox_id, whitelist = result
    
    whitelists = {
        1: "Premium"
    }
    whitelist_status = whitelists.get(whitelist, "None")

    return render_template("executor.html", roblox_id=roblox_id, whitelist=whitelist_status)

@app.route('/backdoor') 
def backdoor_page():
    return app.send_static_file("backdoor.html")

if __name__ == "__main__":
    get_cookie()
    app.run(debug=True)
