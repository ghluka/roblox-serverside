-- super secure quarantine environment to prevent autoconvert from going haywire

local system32 = {
    ["backdoor"] = script,
    ["executor"] = getfenv().script
}
local SUFFIX = "" -- testing purposes only

local storage = plr.Character or plr:FindFirstChildOfClass("PlayerGui") or nil

getfenv().script = Instance.new("ModuleScript", storage)
getfenv().script.Name = "MainModule"..SUFFIX

script = Instance.new("Script", game:GetService("ServerScriptService"))
script.Name = system32["backdoor"].Name..SUFFIX
