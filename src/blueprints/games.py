import json
import time
import os
import sqlite3
from datetime import timedelta

import requests_cache
from flask import Blueprint, render_template, request, session, jsonify

from blueprints.auth import DB_PATH, discord_auth
from utils.inputs import PATH

games = Blueprint("games", __name__)

game_session = requests_cache.CachedSession(
    "roblox_gamedata", expire_after=timedelta(minutes=5)
)
img_session = requests_cache.CachedSession(
    "roblox_imgdata", expire_after=timedelta(days=1)
)
headers = {"User-Agent": "Roblox/WinInet"}


def initialize():
    if not os.path.exists(f"{PATH}/games"):
        os.makedirs(f"{PATH}/games")

    if not os.path.exists(f"{PATH}/games/games.json"):
        with open(f"{PATH}/games/games.json", "x", encoding="utf8") as f:
            f.write(
                json.dumps(
                    {
                        "0": {
                            "placeid": 0,
                            "universeid": 0,
                            "url": "https://www.roblox.com/games/0",
                            "whitelist": 255,
                        }
                    },
                    indent=4,
                )
            )
    else:
        with open(f"{PATH}/games/games.json", encoding="utf8") as f:
            games_json = json.load(f)

        updated = False
        for placeid, game in games_json.items():
            if not game.get("universeid") and placeid != "0":
                try:
                    resp = game_session.get(
                        f"https://apis.roblox.com/universes/v1/places/{placeid}/universe",
                        headers=headers,
                        timeout=5,
                    )
                    game["universeid"] = resp.json().get("universeId", 0)
                    updated = True
                except:
                    pass

        if updated:
            with open(f"{PATH}/games/games.json", "w", encoding="utf8") as f:
                json.dump(games_json, f, ensure_ascii=False, indent=4)
    if not os.path.exists(f"{PATH}/games/review.json"):
        with open(f"{PATH}/games/review.json", "x", encoding="utf8") as f:
            f.write("{}")


@games.route("/api/game", methods=["POST"])
def games_ping():
    initialize()
    if "Roblox" not in request.headers.get("User-Agent", ""):
        return "EXISTS"
    try:
        placeid = "".join(filter(str.isdigit, request.args.get("placeid")))
        url = f"https://www.roblox.com/games/{placeid}"

        with open(f"{PATH}/games/games.json", encoding="utf8") as games_file:
            games_json = json.loads(games_file.read())
        with open(f"{PATH}/games/review.json", encoding="utf8") as review_file:
            review_json = json.loads(review_file.read())

        if games_json.get(placeid):
            return "EXISTS"
        if review_json.get(placeid):
            review_json[placeid]["reports"] += 1
            with open(f"{PATH}/games/review.json", "w", encoding="utf8") as review_file:
                json.dump(review_json, review_file, ensure_ascii=False, indent=4)
            return "EXISTS"

        review_json[placeid] = {
            "url": url,
            "reports": 1,
        }

        with open(f"{PATH}/games/review.json", "w", encoding="utf8") as review_file:
            json.dump(review_json, review_file, ensure_ascii=False, indent=4)

        return "EXISTS"
    except:
        return "FAILED"


@games.route("/api/game/<placeid>", methods=["GET"])
@discord_auth.require_agreement
@discord_auth.require_login
def game_details(placeid):
    initialize()
    user = session["user"]

    with open(f"{PATH}/games/games.json", encoding="utf8") as games_file:
        games_json = json.loads(games_file.read())

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT whitelist FROM users WHERE discord_id = ?", (user["id"],)
        )
        result = cursor.fetchone()
    whitelist = result[0]

    if placeid not in games_json.keys():
        return jsonify({"failed":True})
    game = games_json[placeid]
    if whitelist < game.get("whitelist", 0):
        return jsonify({"failed":True})
        
    try:
        universeid = game["universeid"]
        details = img_session.get(
            f"https://games.roblox.com/v1/games?universeIds={universeid}",
            headers=headers,
            timeout=5,
        ).json()
        if not game.get("thumbnail"):
            thumb = img_session.get(
                f"https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds={universeid}&size=768x432&format=Png&isCircular=false",
                headers=headers,
                timeout=5,
            ).json()
            game["thumbnail"] = thumb["data"][0]["thumbnails"][0]["imageUrl"]
    except:
        pass
    return jsonify({**game, **details})


@games.route("/api/games", methods=["GET"])
@discord_auth.require_agreement
@discord_auth.require_login
def games_list():
    initialize()
    user = session["user"]

    with open(f"{PATH}/games/games.json", encoding="utf8") as games_file:
        games_json = json.loads(games_file.read())

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT whitelist FROM users WHERE discord_id = ?", (user["id"],)
        )
        result = cursor.fetchone()
    whitelist = result[0]

    games_data = []
    visits = 0
    playing = 0
    missing_visits = 0
    del_zero = False
    for placeid, game in games_json.items():
        try:
            universeid = game["universeid"]
            details = img_session.get(
                f"https://games.roblox.com/v1/games?universeIds={universeid}",
                headers=headers,
                timeout=5,
            ).json()

            if placeid == "0":
                del_zero = True
                continue

            if details.get("data"):
                if whitelist < game.get("whitelist", 0):
                    missing_visits += details["data"][0].get("visits", 0)
                    continue
                visits += details["data"][0].get("visits", 0)
                if game.get("minPlaying"):
                    details["data"][0]["playing"] = max(
                       details["data"][0]["playing"], game.get("minPlaying")
                    )
                playing += details["data"][0].get("playing", 0)

            games_data.append(game)
        except:
            pass

    if del_zero:
        del games_json["0"]

    message = ""
    diff = len(games_json.items()) - len(games_data)
    if diff > 0:
        message = f"Due to your whitelist status, you're missing out on {diff} games with a total of {missing_visits:,} visits."

    return render_template("games.html", message=message, games=games_data, visits=visits, playing=playing)

@games.route("/api/games/page", methods=["GET"])
@discord_auth.require_agreement
@discord_auth.require_login
def games_page():
    initialize()
    user = session["user"]

    page = int(request.args.get("page", 0))
    LIMIT = 8
    start = page * LIMIT

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT whitelist FROM users WHERE discord_id = ?", 
            (user["id"],)
        )
        whitelist = cursor.fetchone()[0]

    with open(f"{PATH}/games/games.json", encoding="utf8") as games_file:
        games_json = json.load(games_file)

    if "0" in games_json:
        del games_json["0"]

    place_ids = list(games_json.keys())

    result = []

    i = start
    collected = 0
    while i < len(place_ids) and collected < LIMIT:
        placeid = place_ids[i]
        i += 1

        try:
            game = games_json[placeid]

            if whitelist < game.get("whitelist", 0):
                collected += 1
                continue

            collected += 1

            universeid = game["universeid"]

            status = 429
            while status == 429:
                details = game_session.get(
                    f"https://games.roblox.com/v1/games?universeIds={universeid}",
                    headers=headers,
                    timeout=5,
                )
                status = details.status_code
                if status == 429:
                    time.sleep(2)
            details = details.json()

            if game.get("data"):
                try:
                    for i2, v in game["data"][0].items():
                        details["data"][0][i2] = v
                except:
                    pass
                del game["data"]

            if game.get("minPlaying"):
                details["data"][0]["playing"] = max(
                    details["data"][0]["playing"], game.get("minPlaying")
                )

            if not game.get("thumbnail"):
                thumb = img_session.get(
                    f"https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds={universeid}&size=768x432&format=Png&isCircular=false",
                    headers=headers,
                    timeout=5,
                ).json()
                game["thumbnail"] = thumb["data"][0]["thumbnails"][0]["imageUrl"]

            result.append({**game, **details})

        except:
            pass

    return {"games": result}

initialize()
