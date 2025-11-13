local _env = getfenv()
local Loader = require(tonumber("136871543208848"))
local Ception = require(tonumber("78342552407113"))

local function ValidLuauBytecode(bytecode)
    if type(bytecode) ~= "string" or #bytecode == 0 then
        return false
    end
    return true
end

function luau_compile(source, chunkname)
    local ok, bytecode = pcall(function()
        return Ception.luau_compile(source)
    end)
    if not ok or type(bytecode) ~= "string" then
        return source
    end
    return bytecode
end

function luau_load(bytecode, env)
    assert(ValidLuauBytecode(bytecode), "luau_load: Argument #1 got invalid bytecode")
    assert(type(env) == "table" or env == nil, ("luau_load: Argument #2 got '%s' (table expected)"):format(type(env)))

    local ok, chunk = pcall(function()
        return Loader.luau_load(bytecode, env or _env)
    end)

    if not ok or type(chunk) ~= "function" then
        local f, err = loadstring(bytecode)
        if not f then error(err, 0) end
        setfenv(f, env or _env)
        return f
    end

    return chunk
end

local ls = setmetatable({
    luau_compile = luau_compile,
    luau_load = luau_load,
    luau_execute = function(source, env, chunkname)
        if ValidLuauBytecode(source) and not source:find("\n") then
            return luau_load(source, env)
        end
        return luau_load(luau_compile(source, chunkname), env or _env)
    end,
    create_env = function(envwriter)
        local fenv = _env
        local env = setmetatable({}, {
            __index = function(self, k)
                return envwriter[k] or fenv[k]
            end,
        })
        return env
    end,
}, {
    __call = function(self, source, env, chunkname)
        return self.luau_execute(source, env or _env, chunkname)
    end,
})

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
