
local gui = plr:FindFirstChildOfClass("PlayerGui")
local script = gui:FindFirstChild("_temp")
if not (script and script:IsA("LocalScript")) then
    script = Instance.new("LocalScript", gui)
    script.Name = "_temp"
end

setfenv(1, setmetatable({script = script, owner = plr}, {__index = getfenv()}))

-- 0x24616E567 for Nebula
-- 0x4704B1128689 for Sensation
require(0x4704B1128689)()

-- APPLY ENVIRONMENT CHANGES
game = getfenv(1).game
Game = game
Instance = getfenv(1).Instance
LoadLibrary = getfenv(1).LoadLibrary
if conversion == 0x4704B1128689 then
    PhysicalProperties = getfenv(1).PhysicalProperties
    Raindrop = getfenv(1).Raindrop
    error = getfenv(1).error
    getmetatable = getfenv(1).getmetatable
    loadstring = getfenv(1).loadstring
    print = getfenv(1).print
    require = getfenv(1).require
    setmetatable = getfenv(1).setmetatable
    type = getfenv(1).type
    typeof = getfenv(1).typeof
    warn = getfenv(1).warn
    workspace = getfenv(1).workspace
elseif conversion == 0x24616E567 then
    CFrame = getfenv(1).CFrame
    Camera = getfenv(1).Camera
    Vector3 = getfenv(1).Vector3
    Wrap = getfenv(1).Wrap
    math = getfenv(1).math
end

