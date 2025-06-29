
targets = {{}}

local function findPlayersByUsername(partialName)
    local players = game.Players:GetPlayers()
    local matchingPlayers = {}
    local partialNameLower = string.lower(partialName)

    for _, player in ipairs(players) do
        local playerNameLower = string.lower(player.Name)
        if string.find(playerNameLower, partialNameLower) then
            table.insert(matchingPlayers, player)
        else
            playerNameLower = string.lower(player.DisplayName)
            if string.find(playerNameLower, partialNameLower) then
                table.insert(matchingPlayers, player)
            end
        end
    end

    return matchingPlayers
end

if target == "me" or string.gsub(target, " ", "") == "" then
    table.insert(targets, plr)
elseif target == "all" then
    targets = game:GetService("Players"):GetPlayers()
elseif target == "others" then
    targets = game:GetService("Players"):GetPlayers()
    table.remove(targets, table.find(targets, plr))
else
    targets = findPlayersByUsername(target)
end

for _,target in pairs(targets) do
    if type(target) == "userdata" then
        target = target.Name
    end

    if type(m) == "table" then
        for i,v in pairs(m) do
            pcall(v, target)
        end
    elseif type(m) == "function" then
        pcall(m, target)
    end
end
