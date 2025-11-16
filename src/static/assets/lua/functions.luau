
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

local function bruh()
	local sound = Instance.new("Sound", game:GetService("Players").LocalPlayer:FindFirstChildOfClass("PlayerGui"))
	sound.Name = "bruh"
	sound.SoundId = "rbxassetid://6349641063"
	sound:Play()
	sound.Ended:Connect(function()
		sound:Destroy()
	end)
end
