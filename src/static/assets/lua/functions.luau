
local refresh = function(plr)
	local originalCFrame
	if plr.Character then
		local head = plr.Character:FindFirstChild("Head")
		if head then
			originalCFrame = head.CFrame
		end
	end
	plr:LoadCharacterAsync()
	if originalCFrame then
		local head = (plr.Character or plr.CharacterAdded:Wait()):WaitForChild("Head")
		head.CFrame = originalCFrame
	end
end

local printidentity = function()
	print("Current identity is 8")
end
getfenv().printidentity = printidentity

local function bruh()
	local sound = Instance.new("Sound", game:GetService("Players").LocalPlayer:FindFirstChildOfClass("PlayerGui"))
	sound.Name = "bruh"
	sound.SoundId = "rbxassetid://6349641063"
	sound:Play()
	sound.Ended:Connect(function()
		sound:Destroy()
	end)
end
