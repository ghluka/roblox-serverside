
local printidentity = function()
    print("Current identity is 8")
end

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
