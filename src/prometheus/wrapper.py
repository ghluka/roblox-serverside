import os

from utils.inputs import PATH

UPDATE_EACH_TIME = False

PROMETHEUS = f"{PATH}/prometheus/"
SOURCE = f"{PROMETHEUS}source.lua"
OBFUSCATED = f"{PROMETHEUS}source.obfuscated.lua"

def obfuscate(script):
    """
    Obfuscates a LuaU script with Prometheus.
    Returns the path to the obfuscated script.
    """
    if not os.path.exists(f"{PROMETHEUS}prometheus.exe"):
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

    os.system(f"{PROMETHEUS}prometheus.exe --config \"{PROMETHEUS}config.lua\" {SOURCE}")
    return OBFUSCATED
