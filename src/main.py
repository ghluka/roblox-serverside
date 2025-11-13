import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, session
from markupsafe import Markup

from blueprints.auth import auth
from blueprints.dashboard import dash
from blueprints.executor import executor
from blueprints.games import games
from blueprints.modules import scripthub
from blueprints.user import user
from blueprints.admin import admin
from utils.auth import dev_auth
from utils.cookie import get_cookie
from utils.inputs import PATH

app = Flask(__name__, static_url_path="")
app.register_blueprint(auth)
app.register_blueprint(dash, url_prefix="")
app.register_blueprint(executor)
app.register_blueprint(games)
app.register_blueprint(scripthub)
app.register_blueprint(user)
app.register_blueprint(admin)

load_dotenv()
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

with open(f"{PATH}/CNAME", "r", encoding="utf-8") as f:
    domain = f.read().strip()


@app.route("/")
def homepage():
    dashboard_button = "<a class='discord-button' href='/dashboard'><i class='bx bxl-discord-alt'></i> log in with discord</a>"
    if "user" in session:
        dashboard_button = "<a class='dashboard-button' href='/dashboard'><i class='bx bxs-dashboard'></i> dashboard</a>"
    return render_template(
        "index.html",
        dashboard_button=Markup(dashboard_button),
        domain=domain,
        whitelisted="user" in session,
    )


@app.before_request
def check_user_agent():
    embeds = ["discordbot", "twitterbot"]
    user_agent = request.headers.get("User-Agent", "").lower()
    for embed in embeds:
        if embed in user_agent:
            return app.send_static_file("404.html")


@app.errorhandler(404)
def not_found(_):
    return app.send_static_file("404.html")


@app.route("/script")
def admin_script_page():
    return app.send_static_file("script.html")


@app.route("/privacy")
def privacy_policy_page():
    return app.send_static_file("privacy.html")


@app.route("/terms")
def tos_page():
    return app.send_static_file("terms.html")


@app.route("/eula")
def eula_page():
    return app.send_static_file("eula.html")


if __name__ == "__main__":
    get_cookie()
    app.run(debug=True)
