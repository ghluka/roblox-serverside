import os
import subprocess

from utils.inputs import PATH

UPDATE_EACH_TIME = False

PROMETHEUS = f"{PATH}/prometheus/"
CONFIG = f"{PATH}/obfuscator/"
SOURCE = f"{CONFIG}source.lua"
OBFUSCATED = f"{CONFIG}source.obfuscated.lua"


def obfuscate(script):
    """
    Obfuscates a LuaU script with Prometheus.
    Returns the path to the obfuscated script.
    """
    try:
        version = subprocess.run(
            ["lua", "-v"], capture_output=True, text=True, check=True
        )
        if "Lua 5.1" not in version.stderr:
            return None
    except Exception:
        return None
    if UPDATE_EACH_TIME and os.path.exists(OBFUSCATED):
        os.remove(OBFUSCATED)

    if os.path.exists(SOURCE) and os.path.exists(OBFUSCATED):
        with open(SOURCE, "r", encoding="utf-8") as f:
            temp = f.read()
        if temp == script:
            return OBFUSCATED
    with open(SOURCE, "w", encoding="utf-8") as f:
        f.write(script)

    # print(f'lua {PROMETHEUS}cli.lua --config "{CONFIG}config.lua" {SOURCE}')
    os.system(f'lua {PROMETHEUS}cli.lua --config "{CONFIG}config.lua" {SOURCE}')
    return OBFUSCATED
