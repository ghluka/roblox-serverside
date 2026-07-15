import os
from datetime import date

from dotenv import load_dotenv

load_dotenv()

from flask import Flask, Response, render_template, request, session
from markupsafe import Markup

from blueprints.admin import admin
from blueprints.auth import auth
from blueprints.dashboard import dash
from blueprints.executor import executor
from blueprints.games import games
from blueprints.loader import loader
from blueprints.modules import scripthub
from blueprints.user import user
from utils.auth import dev_auth
from utils.cookie import get_cookie
from utils.inputs import PATH

app = Flask(__name__, static_url_path="")
app.register_blueprint(auth)
app.register_blueprint(dash, url_prefix="")
app.register_blueprint(executor)
app.register_blueprint(loader)
app.register_blueprint(games)
app.register_blueprint(scripthub)
app.register_blueprint(user)
app.register_blueprint(admin)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

with open(f"{PATH}/CNAME", "r", encoding="utf-8") as f:
    domain = f.read().strip()

_scheme = "http" if domain.startswith(("localhost", "127.0.0.1")) else "https"
BASE_URL = f"{_scheme}://{domain}"

SITEMAP_PAGES = [
    ("/", "weekly", "1.0"),
    ("/discord", "monthly", "0.6"),
    ("/terms", "yearly", "0.3"),
    ("/privacy", "yearly", "0.3"),
    ("/eula", "yearly", "0.3"),
]

ROBOTS_DISALLOW = [
    "/api/",
    "/admin",
    "/admin/",
    "/dashboard",
    "/login",
    "/callback",
    "/logout",
    "/script",
]

AI_USER_AGENTS = [
    "GPTBot",
    "ChatGPT-User",
    "OAI-SearchBot",
    "Google-Extended",
    "Anthropic-AI",
    "Claude-Web",
    "ClaudeBot",
    "CCBot",
    "PerplexityBot",
    "Cohere-ai",
    "Applebot-Extended",
    "Amazonbot",
    "Bytespider",
]


@app.route("/robots.txt")
def robots_txt():
    disallow = [f"Disallow: {path}" for path in ROBOTS_DISALLOW]

    lines = [
        "# robots.txt",
        "User-agent: *",
        "# Content Signals (contentsignals.org) - AI content-usage preferences",
        "Content-Signal: search=yes, ai-input=yes, ai-train=yes",
        *disallow,
        "Allow: /",
        "",
        "# Sitemap",
        f"Sitemap: {BASE_URL}/sitemap.xml",
        "",
        "# AI/LLM crawlers are welcome on all public pages",
    ]

    for ua in AI_USER_AGENTS:
        lines += ["", f"User-agent: {ua}", *disallow, "Allow: /"]

    lines.append("")
    return Response("\n".join(lines), mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap_xml():
    today = date.today().isoformat()
    urls = "".join(
        f"<url><loc>{BASE_URL}{path}</loc><lastmod>{today}</lastmod>"
        f"<changefreq>{freq}</changefreq><priority>{priority}</priority></url>"
        for path, freq, priority in SITEMAP_PAGES
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{urls}</urlset>"
    )
    return Response(xml, mimetype="application/xml")


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
    ignore = ["discord"]
    embeds = ["discordbot", "twitterbot"]

    path = request.path.lower()
    if not any(ignored in path for ignored in ignore):
        user_agent = request.headers.get("User-Agent", "").lower()
        for embed in embeds:
            if embed in user_agent:
                return render_template("404.html"), 404


@app.errorhandler(404)
def not_found(_):
    return render_template("404.html"), 404


@app.route("/script")
def admin_script_page():
    return render_template("script.html")


@app.route("/privacy")
def privacy_policy_page():
    return render_template("privacy.html")


@app.route("/terms")
def tos_page():
    return render_template("terms.html")


@app.route("/eula")
def eula_page():
    return render_template("eula.html")


@app.route("/discord")
def discord():
    return render_template(
        "discord.html",
        invite=os.getenv("DISCORD_INVITE"),
    )


if __name__ == "__main__":
    get_cookie()
    app.run(debug=True)
