import os

from utils.inputs import PATH

PROMETHEUS = f"{PATH}/prometheus/"
SOURCE = f"{PROMETHEUS}source.lua"

def obfuscate(script):
    """Obfuscates a LuaU script with Prometheus.
    """
    if not os.path.exists(f"{PROMETHEUS}prometheus.exe"):
        return script

    if os.path.exists(SOURCE) and os.path.exists(f"{PROMETHEUS}source.obfuscated.lua"):
        with open(SOURCE, "r", encoding="utf-8") as f:
            temp = f.read()
        if temp == script:
            with open(f"{PROMETHEUS}source.obfuscated.lua", "r", encoding="utf-8") as f:
                return f.read()
    with open(SOURCE, "w", encoding="utf-8") as f:
        f.write(script)

    os.system(f"{PROMETHEUS}prometheus.exe --config \"{PROMETHEUS}config.lua\" {SOURCE}")
    with open(f"{PROMETHEUS}source.obfuscated.lua", "r", encoding="utf-8") as f:
        return f.read()
