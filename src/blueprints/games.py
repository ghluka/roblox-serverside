import json
import os
import random
import secrets
import sqlite3
import time
from datetime import datetime, timedelta

import requests_cache
from flask import Blueprint, jsonify, redirect, render_template, request, session

from blueprints.auth import DB_PATH, discord_auth, domain
from utils.inputs import PATH

games = Blueprint("games", __name__)

LINKVERTISE_ID = os.getenv("LINKVERTISE_ID", "")
KEY_DURATION = timedelta(hours=24)

CHALLENGE_TTL = timedelta(minutes=45)
# CHALLENGE_MIN_AGE = timedelta(seconds=5)

_scheme = "" if domain.startswith(("localhost", "127.0.0.1")) else "s"
VERIFY_TARGET = f"http{_scheme}://{domain}/api/key/verify"

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


def _load_games():
    with open(f"{PATH}/games/games.json", encoding="utf8") as f:
        return json.load(f)


def _level0_pool(games_json):
    """All whitelist-level-0 game place ids, excluding the sentinel entry."""
    return [
        placeid
        for placeid, game in games_json.items()
        if placeid != "0" and game.get("whitelist", 0) == 0
    ]


def _get_user_row(discord_id):
    """(id, whitelist, key_expires, key_game, free_refreshes) for a discord id."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, whitelist, key_expires, key_game, free_refreshes"
            " FROM users WHERE discord_id = ?",
            (discord_id,),
        )
        return cursor.fetchone()


def _key_valid(key_expires):
    if not key_expires:
        return False
    try:
        return datetime.fromisoformat(key_expires) > datetime.utcnow()
    except (ValueError, TypeError):
        return False


def _assign_random_game(discord_id, exclude=None):
    """Assign a random level-0 game to the user, avoiding `exclude` when possible."""
    pool = _level0_pool(_load_games())
    if not pool:
        return None
    if exclude and len(pool) > 1:
        pool = [placeid for placeid in pool if placeid != exclude] or pool
    choice = random.choice(pool)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "UPDATE users SET key_game = ? WHERE discord_id = ?", (choice, discord_id)
        )
        conn.commit()
    return choice


def _game_payload(placeid, games_json):
    """Public-facing details for a single game (name, thumbnail, visits, playing)."""
    game = games_json.get(placeid)
    if not game:
        return None
    payload = {
        "placeid": placeid,
        "url": game.get("url"),
        "thumbnail": game.get("thumbnail"),
        "name": None,
        "creator": None,
        "description": None,
        "visits": 0,
        "playing": 0,
        "favorites": 0,
        "maxplayers": 0,
    }
    try:
        details = img_session.get(
            f"https://games.roblox.com/v1/games?universeIds={game['universeid']}",
            headers=headers,
            timeout=5,
        ).json()
        data = details["data"][0]
        payload["name"] = data.get("name")
        payload["creator"] = (data.get("creator") or {}).get("name")
        payload["description"] = data.get("description")
        payload["visits"] = data.get("visits", 0)
        payload["favorites"] = data.get("favoritedCount", 0)
        payload["maxplayers"] = data.get("maxPlayers", 0)
        playing = data.get("playing", 0)
        if game.get("minPlaying"):
            playing = max(playing, game["minPlaying"])
        payload["playing"] = playing
        if not game.get("thumbnail"):
            thumb = img_session.get(
                f"https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds={game['universeid']}&size=768x432&format=Png&isCircular=false",
                headers=headers,
                timeout=5,
            ).json()
            payload["thumbnail"] = thumb["data"][0]["thumbnails"][0]["imageUrl"]
    except Exception:
        pass
    if game.get("data"):
        try:
            payload["name"] = game["data"][0].get("name") or payload["name"]
        except Exception:
            pass
    return payload


def _get_challenge(discord_id):
    """(key_challenge, key_challenge_time) for a discord id."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT key_challenge, key_challenge_time FROM users WHERE discord_id = ?",
            (discord_id,),
        )
        return cursor.fetchone()


def _challenge_valid(token, challenge):
    """A returned token is valid only if it matches the stored single-use
    challenge and came back within the allowed time window."""
    if not token or not challenge:
        return False
    stored, stored_time = challenge
    if not stored or not secrets.compare_digest(str(stored), str(token)):
        return False
    try:
        age = datetime.utcnow() - datetime.fromisoformat(stored_time)
    except (ValueError, TypeError):
        return False
    # return CHALLENGE_MIN_AGE <= age <= CHALLENGE_TTL
    return age <= CHALLENGE_TTL


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
        return jsonify({"failed": True})
    game = games_json[placeid]
    if whitelist < game.get("whitelist", 0):
        return jsonify({"failed": True})

    if whitelist == 0:
        row = _get_user_row(user["id"])
        if not row or placeid != row[3] or not _key_valid(row[2]):
            return jsonify({"failed": True})

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

    if whitelist == 0:
        row = _get_user_row(user["id"])
        if row and not row[3]:
            _assign_random_game(user["id"])
        return render_template("games_free.html")

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

    return render_template(
        "games.html", message=message, games=games_data, visits=visits, playing=playing
    )


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
            "SELECT whitelist FROM users WHERE discord_id = ?", (user["id"],)
        )
        whitelist = cursor.fetchone()[0]

    if whitelist == 0:
        return {"games": []}

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


@games.route("/api/key/status", methods=["GET"])
@discord_auth.require_agreement
@discord_auth.require_login
def key_status():
    initialize()
    user = session["user"]

    row = _get_user_row(user["id"])
    if not row or row[1] != 0:
        return jsonify({"free_tier": False})

    _, _, key_expires, key_game, free_refreshes = row
    if not key_game:
        key_game = _assign_random_game(user["id"])

    valid = _key_valid(key_expires)
    seconds_left = 0
    if valid:
        seconds_left = max(
            0,
            int(
                (
                    datetime.fromisoformat(key_expires) - datetime.utcnow()
                ).total_seconds()
            ),
        )

    return jsonify(
        {
            "free_tier": True,
            "publisher_id": LINKVERTISE_ID,
            "valid": valid,
            "seconds_left": seconds_left,
            "free_refreshes": free_refreshes or 0,
            "game": _game_payload(key_game, _load_games()) if key_game else None,
        }
    )


@games.route("/api/key/challenge", methods=["GET"])
@discord_auth.require_agreement
@discord_auth.require_login
def key_challenge():
    """Mint a single-use token and return the Linkvertise link target that
    embeds it. The token can only be learned by completing the (v2, encrypted)
    link, so returning it to /api/key/verify proves the flow was completed."""
    user = session["user"]
    row = _get_user_row(user["id"])
    if not row or row[1] != 0:
        return jsonify({"failed": True}), 403

    token = secrets.token_urlsafe(24)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "UPDATE users SET key_challenge = ?, key_challenge_time = ?"
            " WHERE discord_id = ?",
            (token, datetime.utcnow().isoformat(), user["id"]),
        )
        conn.commit()

    return jsonify({"target": f"{VERIFY_TARGET}?token={token}"})


@games.route("/api/key/verify", methods=["GET"])
@discord_auth.require_login
def key_verify():
    user = session["user"]
    row = _get_user_row(user["id"])
    if not row or row[1] != 0:
        return redirect("/dashboard#games")

    token = request.args.get("token", "")
    if not _challenge_valid(token, _get_challenge(user["id"])):
        return redirect("/dashboard?key=failed#games")

    expires = (datetime.utcnow() + KEY_DURATION).isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "UPDATE users SET key_expires = ?, free_refreshes = 1,"
            " key_challenge = NULL, key_challenge_time = NULL WHERE discord_id = ?",
            (expires, user["id"]),
        )
        conn.commit()
    if not row[3]:
        _assign_random_game(user["id"])

    return redirect("/dashboard?key=success#games")


@games.route("/api/key/refresh", methods=["POST"])
@discord_auth.require_agreement
@discord_auth.require_login
def key_refresh():
    user = session["user"]
    row = _get_user_row(user["id"])
    if not row or row[1] != 0:
        return jsonify({"failed": True}), 403

    _, _, key_expires, key_game, free_refreshes = row
    if not _key_valid(key_expires) or (free_refreshes or 0) <= 0:
        return jsonify({"failed": True, "reason": "no_refresh"}), 403

    new_game = _assign_random_game(user["id"], exclude=key_game)
    remaining = (free_refreshes or 1) - 1
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "UPDATE users SET free_refreshes = ? WHERE discord_id = ?",
            (remaining, user["id"]),
        )
        conn.commit()

    return jsonify(
        {"game": _game_payload(new_game, _load_games()), "free_refreshes": remaining}
    )


initialize()
