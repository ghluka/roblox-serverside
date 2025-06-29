local _env = getfenv()

local compile = require(125795446062284)
local fione = require(100935166061231)
local createExecutable = function(bCode, env)
	return fione.wrap_lua(fione.stm_lua(bCode), env or _env)
end

local ls = function(source, env)
	local executable
	local env = env or _env
	local name = (env.script and env.script:GetFullName())

	compile = require(125795446062284)
	fione = require(100935166061231)

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
	game = _env.game
	Game = game
	Instance = _env.Instance
	CFrame = _env.CFrame
	Vector3 = _env.Vector3
	math = _env.math
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