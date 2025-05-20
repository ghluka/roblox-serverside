local env = require(104710331237296)

local compile = require(125795446062284)
local fione = require(100935166061231)
local createExecutable = function(bCode, env)
	return fione.wrap_lua(fione.stm_lua(bCode), env or getfenv(0))
end

local ls = function(source, env)
	local executable
	local env = env or getfenv(2)
	local name = (env.script and env.script:GetFullName())
	local ran, failureReason = pcall(function()
		local compiledBytecode = compile(source, name)
		executable = createExecutable(compiledBytecode, env)
	end)

	if ran then
		return setfenv(executable, env)
	end
	return nil, failureReason
end


local function fixenv()
	game = env.game
	Game = game
	Instance = env.Instance
	CFrame = env.CFrame
	Vector3 = env.Vector3
	math = env.math
end

local run = function(source)
	local o
	local loadstringEnabled = pcall(function() loadstring("_ = true")() end)
	fixenv()
	if not loadstringEnabled then
		o = ls(source)()
	else
		o = loadstring(source)()
	end
	fixenv()
	
	return function()
		return
	end
end