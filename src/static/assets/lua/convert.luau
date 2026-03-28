
getfenv(1).owner = plr

if plr.Character and plr.Character.Parent ~= nil then
    -- 0x24616E567 for Nebula
    -- 0x55262CE723BF for Sensation
    local conversion = 0x24616E567
    require(conversion)()
end

-- APPLY ENVIRONMENT CHANGES
game = getfenv(1).game
Game = game
Instance = getfenv(1).Instance
LoadLibrary = getfenv(1).LoadLibrary
if conversion == 0x55262CE723BF then
    PhysicalProperties = getfenv(1).PhysicalProperties
    Raindrop = getfenv(1).Raindrop
    getmetatable = getfenv(1).getmetatable
    loadstring = getfenv(1).loadstring
    require = getfenv(1).require
    setmetatable = getfenv(1).setmetatable
    type = getfenv(1).type
    typeof = getfenv(1).typeof
    workspace = getfenv(1).workspace
elseif conversion == 0x24616E567 then
    CFrame = getfenv(1).CFrame
    Camera = getfenv(1).Camera
    Vector3 = getfenv(1).Vector3
    Wrap = getfenv(1).Wrap
    math = getfenv(1).math
end
print = getfenv(1).print
warn = getfenv(1).warn
error = getfenv(1).error

getfenv().script.Parent = system32["backdoor"]
system32 = nil -- stop ppl from accessing!

-- extra conversions that nebula doesnt do:
local wrapObject = getfenv().Wrap
local function fauxWrap(obj)
	function obj:FindFirstChild(...)
		return obj.real:FindFirstChild(...)
	end
end
getfenv().Wrap = function(v)
	local obj = wrapObject(v)
	fauxWrap(obj)
	return obj
end

local Instance_new = Instance.new
local Instance = table.clone(Instance)
local function fauxBin(tool)
	tool.Name = "HopperBin"
	tool.RequiresHandle = false

	local faux = getfenv().Wrap(tool)
	faux.ClassName = "HopperBin"

	function faux:GetChildren()
		return tool:GetChildren()
	end

	function faux:FindFirstChild(name)
		return tool:FindFirstChild(name)
	end

	function faux:IsA(class)
		return class == "HopperBin" or tool:IsA(class)
	end

	function faux:Destroy()
		tool:Destroy()
	end

	setmetatable(faux, {
		__index = function(_, k)
			if k == "Name" then
				return tool.Name
			elseif k == "Parent" then
				return tool.Parent
			elseif k == "BinType" then
				return faux._binType or Enum.BinType.Script
			elseif k == "Active" then
				return faux._active or false
			elseif k == "Selected" then
				return faux._selectedEvent
			elseif k == "Deselected" then
				return faux._deselectedEvent
			elseif k == "Tool" then
				return tool
			else
				return rawget(faux, k)
			end
		end,
		__newindex = function(_, k, v)
			if k == "Name" then
				tool.Name = v
			elseif k == "Parent" then
				tool.Parent = v
			elseif k == "BinType" then
				faux._binType = v
			elseif k == "Active" then
				faux._active = v
			elseif (v and typeof(v)=='table' and v.real) then
				tool[k]=v.real
			else
				rawset(faux, k, v)
			end
		end
	})

	local selectedEvent = {}
	selectedEvent.Queue = 0
	local deselectedEvent = Instance_new("BindableEvent")
	faux._deselectedEvent = deselectedEvent.Event
	local m
	pcall(function()
		m = game:GetService("Players").LocalPlayer:GetMouse()
	end)

	function selectedEvent:Connect(func)
		local discon = {}
		local disconnect = false
		coroutine.wrap(function()
			while task.wait() do
				if disconnect then 
					for i in m do
						pcall(function()
							m[i]["_connections"] = {}
							m[i]["_yield"] = {}
						end)
					end
					break
				end
				if selectedEvent.Queue > 0 then
					selectedEvent.Queue -= 1
					coroutine.wrap(function()
						func(m)
					end)()
				end
			end
		end)()
		function discon:Disconnect()
			disconnect = true
		end
		return discon
	end
	function selectedEvent:Once(func)
		local discon = {}
		local disconnect = false
		coroutine.wrap(function()
			while task.wait() do
				if disconnect then 
					for i in m do
						pcall(function()
							m[i]["_connections"] = {}
							m[i]["_yield"] = {}
						end)
					end
					break
				end
				if selectedEvent.Queue > 0 then
					selectedEvent.Queue -= 1
					coroutine.wrap(function()
						func(m)
					end)()
					break
				end
			end
		end)()
		function discon:Disconnect()
			disconnect = true
		end
		return discon
	end
	function selectedEvent:connect(func)
		return selectedEvent:Connect(func)
	end

	faux._selectedEvent = selectedEvent

	tool.Equipped:Connect(function(mouse)
		faux._active = true
		selectedEvent.Queue += 1
	end)
	tool.Unequipped:Connect(function()
		faux._active = false
		for i in m do
			pcall(function()
				m[i]["_connections"] = {}
				m[i]["_yield"] = {}
			end)
		end
		deselectedEvent:Fire()
	end)

	function faux:Clone()
		return fauxBin(tool)
	end

	faux.Selected = faux._selectedEvent
	faux.Deselected = faux._deselectedEvent

	return faux
end

script = getfenv().Wrap(script)
script.Parent = script.real.Parent

local realGame = game
local fakeGame={real=realGame};

local fakes={}
local reals = {}

local function getReal(i)
	return fakes[i] or i
end
local newObject = function()
	local object = {}			
	object.__index=function(self,idx)
		local val = rawget(self,idx);
		if(typeof(val)=="function")then
			return function(self2,...)
				local realFunc = rawget(self,"real")[idx]==val
				if(realFunc and self2==self)then
					self2=rawget(self,"real")
				end
				local ret = val(self2,...)
				if(typeof(ret)=="Instance")then
					local w,s = getfenv().Wrap(ret)
					if(s)then ret = w end
				end
				return ret
			end
		end
		if(typeof(val)=="Instance" and val~=rawget(self,"real"))then
			local w,s = getfenv().Wrap(val)
			if(s)then val = w end
		end
		return val
	end
	object.__newindex=function(self,idx,val)
		if(val and typeof(val)=="table" and val.real)then
			getReal(self)[idx]=val.real
		else
			getReal(self)[idx]=getReal(val)
		end
	end
	object.__type="Instance"
	object.__tostring=function(self)
		return rawget(self,"real").Name
	end
	return object
end

Instance.new = function(className, parent)
	if type(parent) == "table" and parent.real then
		parent = parent.real
	end
	if className == "HopperBin" then
		return fauxBin(Instance_new("Tool", parent))
	end

	return Instance_new(className, parent)
end

local CoreGui = {}
local coreGui
pcall(function()
	local function generateCoreGui()
		{{coreGui}}
	end
	for _,v in pairs(realGame:service("Players").LocalPlayer:FindFirstChildOfClass("PlayerGui"):GetChildren()) do -- inefficient but safest option?
		if v.Name == "CoreGui" and v:IsA("Folder") and v:GetAttribute("NETTWTF") then
			CoreGui = {CoreGui = v}
		end
	end
	if not CoreGui.CoreGui then
		CoreGui = generateCoreGui()
	end
	coreGui = CoreGui.CoreGui
	coreGui.Parent = realGame:service("Players").LocalPlayer:FindFirstChildOfClass("PlayerGui")
end)

local log4j = {
	real=realGame["LogService"]
}
local log4shell = game:GetService("LogService")
log4j.Name = "LogService"
log4j.MessageOut = {}
function log4j.MessageOut:Connect(callback)
	local con = log4shell.MessageOut:Connect(function(msg, mt)
		if msg == "using EzConvert by "..game:service'Players':GetNameFromUserIdAsync(5719877) then
			-- get ignored xD
		elseif not(mt == Enum.MessageType.MessageOutput and
			string.sub(msg, 1, 16) == "Requiring asset ") then
			callback(msg, mt)
		else
			callback("Requiring asset [REDACTED].", mt)
		end
	end)
	return {
		Disconnect = function()
			con:Disconnect()
		end
	}
end
function log4j.MessageOut:Once(callback)
	local con
	con = log4j.MessageOut:Connect(function(msg, mt)
		callback(msg, mt)
		con:Disconnect()
	end)
end
function log4j.MessageOut:Wait()
	return log4shell.MessageOut:Wait()
end
local log4shell = nil

local services = {
	LogService=log4j;
	Players=realGame:service'Players';
}
if plr.Character and plr.Character.Parent ~= nil then
	services = {
		CoreGui=coreGui;
		Players=realGame:service'Players';
		UserInputService=realGame.UserInputService;
		Debris=realGame.Debris;
		LogService=log4j;
		--Workspace={CurrentCamera=FakeCam,real=workspace};
		RunService={
			_bound={},
			_lastCall=tick();
			real=realGame["Run Service"],
			Stepped=realGame["Run Service"].real.Stepped,
			RenderStepped=realGame["Run Service"].Stepped,
			Heartbeat=game:service'RunService'.Stepped,
		};
	}
end

local function getService(self,name)
	if(self==fakeGame)then
		return services[name] or realGame:service(name)
	end
end

fakeGame.service=getService;
fakeGame.GetService=getService;
for i,v in next, services do
	if type(v) == "table" then
		fakes[v]=v.real
		fakeGame[v.real.Name]=v
	elseif typeof(v) == "Instance" then
		fakes[v]=v
		fakeGame[v.Name]=v
	end
end

function fakeGame:HttpGet(url:string, synchronous:bool, httpRequestType:Enum.HttpRequestType, doNotAllowDiabolicalMode:bool)
	return realGame:GetService("HttpService"):GetAsync(url)
end

fauxWrap(fakeGame)
setmetatable(fakeGame,newObject())
fakes[fakeGame]=game
game = fakeGame
Game = game

local realGame = game

local function buildOutput(...)
	local parts = {}
	for _,v in pairs({...}) do
		table.insert(parts, tostring(v))
	end
	return table.concat(parts, " ")
end

local err = error
print = function(...)
	local out = buildOutput(...)
	pcall(function()
		require(tonumber("130629305657257"))(plr, "print", out)
		getfenv(2).print(out)
	end)
end
warn = function(...)
	local out = buildOutput(...)
	pcall(function()
		require(tonumber("130629305657257"))(plr, "warn", out)
		getfenv(2).warn(out)
	end)
end
error = function(...)
	local out = buildOutput(...)
	pcall(function()
		require(tonumber("130629305657257"))(plr, "error", out)
	end)
	err()
end

-- allow functions to be accessible from loadstring
getfenv().game = game
getfenv().Game = game
getfenv().print = print
getfenv().warn = warn
getfenv().error = error
getfenv().Instance = Instance
