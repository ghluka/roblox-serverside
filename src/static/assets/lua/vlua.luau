local _env = getfenv()

local function getCallerEnv(level)
	level = (level or 1) + 1
	if debug.info then
		local fn = debug.info(level, 'f')
		return getfenv(fn)
	else
		local info = debug.getinfo(level, 'f')
		if not info or not info.func then
			return getfenv(0)
		end
		return getfenv(info.func)
	end
end

local function init_vluau(Loader, Ception)
	local function createSettings()
		return {
			vectorCtor = Vector3 and Vector3.new or function() error("vectorCtor was not provided") end,
			vectorSize = 3,
			useNativeNamecall = false,
			namecallHandler = function() error("Native __namecall handler was not provided") end,
			extensions = {},
			callHooks = {},
			errorHandling = false,
			generalizedIteration = false,
			allowProxyErrors = false,
			useImportConstants = false,
			staticEnvironment = {},
			decodeOp = function(op) return op end
		}
	end

	local default_settings = createSettings()

	local function getType(v)
		if typeof then
			return typeof(v)
		end
		return type(v)
	end

	local function readByte(bc, index)
		if buffer and getType(bc) == 'buffer' then
			return buffer.readu8(bc, index)
		end
		return string.byte(bc, index + 1)
	end

	local function ValidLuauBytecode(bytecode)
		if #bytecode == 0 then
			return false
		end

		local bc = bytecode
		if buffer and getType(bytecode) == 'string' then
			bc = buffer.fromstring(bytecode)
		end

		local luauVersion = readByte(bc, 0)
		if luauVersion == 0 then
			--error("the provided bytecode is an error message",0)
			return false
		elseif luauVersion < 3 or luauVersion > 6 then
			--error("the version of the provided bytecode is unsupported",0)
			return false
		elseif luauVersion >= 4 then
			return true
		end
		return true
	end

	function luau_compile(source, chunkname)
		local bytecode, _ = Ception.luau_compile(source)
		if bytecode:sub(1, 1) ~= "\0" then
			return bytecode
		else
			error((chunkname or '@') .. bytecode:sub(2), 0)
		end
	end

	function luau_load(bytecode, env, settings)
		assert(ValidLuauBytecode(bytecode), "luau_load: Argument #1 got invalid bytecode")
		assert(type(env) == 'table' or env == nil, ("luau_load: Argument #2 got '%s' (table expected)"):format(getType(env)))
		return Loader.luau_load(bytecode, env or getCallerEnv(2), settings or default_settings)
	end

	return setmetatable({
		luau_compile = luau_compile,
		luau_load = luau_load,
		luau_execute = function(source, env, chunkname, settings)
			if ValidLuauBytecode(source) then
				return luau_load(source, env, settings)
			end
			return luau_load(luau_compile(source, chunkname), env or getCallerEnv(2), settings)
		end,
		create_env = function(envwriter)
			local fenv = getCallerEnv(2)
			local env = setmetatable({}, {
				__index = function(self, k)
					return envwriter[k] or fenv[k]
				end,
			})
			return env
		end,
		create_settings = createSettings
	}, {
		__call = function(self, source, env, chunkname)
			return self.luau_execute(source, env or getCallerEnv(2), chunkname)
		end,
	})
end

local function make_sandbox()
	local real = _env
	local env = {}
	setmetatable(env, {
		__index = function(_, k)
			return real[k]
		end,
		__newindex = function(t,k,v) rawset(t,k,v) end,
	})
	env._G = env
	env._ENV = env
	return env
end

local ls
--local luavms = table.create(0)
--luavms[1] = "123167605868335"
--for _,luavm in pairs(luavms) do
--	if pcall(function()
--			local vluau = require(tonumber(luavm))
--			ls = function(source, env, chunkname)
--				return vluau.luau_execute(source, env or getCallerEnv(2), chunkname)
--			end
--		end) then
--		break
--	end
--end

if not ls then
	local ceptions = table.create(0)
	ceptions[1] = "78342552407113"
	ceptions[2] = "86277566190608"
	local fius = table.create(0)
	fius[1] = "136871543208848"
	fius[2] = "131963555187801"
	for _,ception in pairs(ceptions) do
		local ception = require(tonumber(ception))
		for _,fiu in pairs(fius) do
			local fiu = require(tonumber(fiu))
			if pcall(function()
					init_vluau(fiu, ception)
				end)
			then
				ls = init_vluau(fiu, ception)
				break
			end
		end
	end
end

local run = function(source)
	local env = make_sandbox()

	env.game = _env.game
	env.Instance = _env.Instance
	env.CFrame = _env.CFrame
	env.Vector3 = _env.Vector3
	env.math = _env.math

	local chunk = ls(source, env)
	if type(chunk) ~= "function" then
		warn("failed to compile chunk", 0)
	end

	local ok, res = pcall(chunk)
	if not ok then
		warn(res, 0)
	end

	return res
end
