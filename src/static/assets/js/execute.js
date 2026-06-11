const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

function trackExecution() {
    const count = (parseInt(localStorage.getItem('nettss_executed') || '0')) + 1;
    localStorage.setItem('nettss_executed', count);
    const el = document.getElementById('stat-scripts');
    if (el) el.textContent = count.toLocaleString();
}

function execute(script) {
    const url = window.location.origin + "/api/execute";

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "text/plain"
        },
        body: script
    }).then(response => response.text()).then(function(response) {
        if (response == "NO CLIENT") {
            userIdAlert(getUserId());
        } else {
            trackExecution();
        }
    }).catch(error => console.error('Error:', error));
}

function executeSS(script) {
    const url = window.location.origin + "/api/execute_ss";
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "text/plain"
        },
        body: script
    }).then(response => response.text()).then(function(response) {
        if (response == "NO CLIENT") {
            userIdAlert(getUserId());
        } else {
            trackExecution();
        }
    }).catch(error => console.error('Error:', error));
}

function executeRequire(script)
{
    let targets = [];
    if (typeof window.getModuleTargets === "function") {
        targets = window.getModuleTargets();
    }

    if (targets.length === 0) {
        const usernameEl = document.getElementById("username");
        targets = [usernameEl ? usernameEl.textContent.trim() : ""];
    }

    targets.forEach(username => {
        const url = window.location.origin + "/api/execute_module?username=" + encodeURIComponent(username);
        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "text/plain"
            },
            body: script
        }).then(response => response.text()).then(function(response) {
            if (response == "NO CLIENT") {
                userIdAlert(getUserId());
            } else {
                trackExecution();
            }
        }).catch(error => console.error('Error:', error));
    });
}

function executePlayerAction(script) {
    const targetid = document.getElementById("player-actions").getAttribute("userid");
    
    script = "local targethum = targetchar:FindFirstChildOfClass('Humanoid')\n" + script
    script = "local targetchar = target.Character\n" + script
    script = "local target = game:GetService('Players'):GetPlayerByUserId(" + targetid + ")\n" + script
    script = "local plrchar = plr.Character\n" + script
    script = "local plr = game:GetService('Players'):GetPlayerByUserId(" + getUserId() + ")\n" + script
    
    execute(script);
}
