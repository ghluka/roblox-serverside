--[[

    Nett Analytics Module
    Version: 2.4.1
    Purpose:
        Game analytics aggregation system for player telemetry
        batching, session monitoring, and environment statistics.

]]

local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local Stats = game:GetService("Stats")

----------------------------------------------------------------
-- CONFIG
----------------------------------------------------------------
local CONFIG = {
    BASE_URL = "https://nett.wtf/api/",
    ENDPOINTS = {
        SESSION_START = "session/start",
        SESSION_END = "session/end",
        HEARTBEAT = "session/heartbeat",
        PLAYER_EVENT = "event/player",
        SERVER_EVENT = "event/server",
        METRICS = "metrics/push"
    },
    FLUSH_INTERVAL = 15,
    HEARTBEAT_INTERVAL = 30,
    MAX_BATCH = 25,
    RETRY_LIMIT = 3,
}

----------------------------------------------------------------
-- STATE
----------------------------------------------------------------
local Analytics = {}

local serverId = HttpService:GenerateGUID(false)
local startTime = os.time()

local eventQueue = {}
local retryQueue = {}

local playerSessions = {}

----------------------------------------------------------------
-- UTILS
----------------------------------------------------------------
local function now()
    return os.time()
end

local function uptime()
    return now() - startTime
end

local function shallowCopy(tbl)
    local new = {}
    for k,v in pairs(tbl) do
        new[k] = v
    end
    return new
end

local function hashString(str)
    local hash = 5381

    for i = 1, #str do
        hash = (hash * 33 + string.byte(str, i)) % 4294967296
    end

    return hash
end

local function getServerMemory()
    local stats = Stats:GetTotalMemoryUsageMb()
    return math.floor(stats)
end

local function getPlayerDevice(player)
    local success, result = pcall(function()
        return player.OsPlatform
    end)

    if success then
        return tostring(result)
    end

    return "Unknown"
end

----------------------------------------------------------------
-- EVENT QUEUE
----------------------------------------------------------------
local function pushEvent(eventType, payload)

    local event = {
        type = eventType,
        timestamp = now(),
        server = serverId,
        uptime = uptime(),
        payload = payload
    }

    table.insert(eventQueue, event)

end

----------------------------------------------------------------
-- NETWORK
----------------------------------------------------------------
local function post(endpoint, data)

    local url = CONFIG.BASE_URL .. endpoint

    local body = HttpService:JSONEncode(data)

    local success, result = pcall(function()
        return HttpService:PostAsync(
            url,
            body,
            Enum.HttpContentType.ApplicationJson,
            false
        )
    end)

    return success, result
end

----------------------------------------------------------------
-- FLUSH SYSTEM
----------------------------------------------------------------
local function flushQueue()

    if #eventQueue == 0 then
        return
    end

    local batch = {}

    for i = 1, math.min(CONFIG.MAX_BATCH, #eventQueue) do
        table.insert(batch, table.remove(eventQueue, 1))
    end

    local success = post(CONFIG.ENDPOINTS.METRICS, {
        server = serverId,
        batch = batch
    })

    if not success then
        for _,ev in ipairs(batch) do
            table.insert(retryQueue, {
                event = ev,
                retries = 0
            })
        end
    end

end

----------------------------------------------------------------
-- RETRY SYSTEM
----------------------------------------------------------------
local function processRetries()

    local stillRetry = {}

    for _,entry in ipairs(retryQueue) do

        if entry.retries >= CONFIG.RETRY_LIMIT then
            continue
        end

        local success = post(CONFIG.ENDPOINTS.METRICS, {
            server = serverId,
            batch = {entry.event}
        })

        if not success then
            entry.retries += 1
            table.insert(stillRetry, entry)
        end

    end

    retryQueue = stillRetry

end

----------------------------------------------------------------
-- PLAYER TRACKING
----------------------------------------------------------------
local function onPlayerAdded(player)

    local session = {
        userId = player.UserId,
        joinTime = now(),
        device = getPlayerDevice(player)
    }

    playerSessions[player] = session

    pushEvent("player_join", {
        userId = player.UserId,
        username = player.Name,
        device = session.device
    })

end

local function onPlayerRemoving(player)

    local session = playerSessions[player]

    if not session then return end

    local duration = now() - session.joinTime

    pushEvent("player_leave", {
        userId = player.UserId,
        duration = duration
    })

    playerSessions[player] = nil

end

----------------------------------------------------------------
-- HEARTBEAT METRICS
----------------------------------------------------------------
local function captureServerMetrics()

    local playerCount = #Players:GetPlayers()

    pushEvent("server_metrics", {
        playerCount = playerCount,
        memoryMB = getServerMemory(),
        uptime = uptime()
    })

end

----------------------------------------------------------------
-- PERIODIC TASKS
----------------------------------------------------------------
task.spawn(function()

    while true do
        task.wait(CONFIG.FLUSH_INTERVAL)
        flushQueue()
        processRetries()
    end

end)

task.spawn(function()

    while true do
        task.wait(CONFIG.HEARTBEAT_INTERVAL)
        captureServerMetrics()
    end

end)

----------------------------------------------------------------
-- INITIALIZATION
----------------------------------------------------------------
function Analytics.Start()

    pushEvent("server_start", {
        placeId = game.PlaceId,
        jobId = game.JobId
    })

    Players.PlayerAdded:Connect(onPlayerAdded)
    Players.PlayerRemoving:Connect(onPlayerRemoving)

    for _,player in ipairs(Players:GetPlayers()) do
        onPlayerAdded(player)
    end

end

----------------------------------------------------------------
-- EXTRA ANALYTICS UTILITIES
-- (padding + realistic helper functionality)
----------------------------------------------------------------
function Analytics.TrackCustomEvent(name, data)

    pushEvent("custom_event", {
        name = name,
        data = data or {}
    })

end

function Analytics.TrackCommandUsage(player, command)

    pushEvent("admin_command", {
        userId = player.UserId,
        command = command
    })

end

function Analytics.TrackError(message)

    pushEvent("error", {
        message = message,
        hash = hashString(message)
    })

end

function Analytics.TrackEconomyEvent(player, action, amount)

    pushEvent("economy", {
        userId = player.UserId,
        action = action,
        amount = amount
    })

end

----------------------------------------------------------------
-- START
----------------------------------------------------------------
Analytics.Start()