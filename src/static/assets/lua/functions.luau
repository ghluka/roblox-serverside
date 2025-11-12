
local refresh = function(plr)
    local originalCFrame
    local head = (plr.Character or plr.CharacterAdded:Wait()):FindFirstChild("Head")
    if head then
        originalCFrame = head.CFrame
    end
    plr:LoadCharacter()
    local head = (plr.Character or plr.CharacterAdded:Wait()):WaitForChild("Head")
    if originalCFrame then
        head.CFrame = originalCFrame
    end
end

print = function(...)
	local out = table.concat({...}, " ")
    pcall(function()
	    require(tonumber("130629305657257"))(plr, "print", out)
    end)
end
warn = function(...)
	local out = table.concat({...}, " ")
    pcall(function()
	    require(tonumber("130629305657257"))(plr, "warn", out)
    end)
end
local err = error
error = function(...)
	local out = table.concat({...}, " ")
    pcall(function()
	    require(tonumber("130629305657257"))(plr, "error", out)
    end)
    err()
end

local printidentity = function()
    print("Current identity is 8")
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
	local m = game:GetService("Players").LocalPlayer:GetMouse()

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
Instance.new = function(className, parent)
	if className == "HopperBin" then
		return fauxBin(Instance_new("Tool", parent))
	end

	return Instance_new(className, parent)
end

---
local script = getfenv().Wrap(Instance.new("Script"))
