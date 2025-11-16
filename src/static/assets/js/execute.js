const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

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
        }
    }).catch(error => console.error('Error:', error));
}

function executeRequire(script)
{
    var username =  document.getElementById("module-username").value;
    if (username == "") {
        var username = document.getElementById("username").innerHTML;
    }
    const url = window.location.origin + "/api/execute_module?username=" + username
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "text/plain"
        },
        body: script
    }).then(response => response.text()).then(function(response) {
        if (response == "NO CLIENT") {
            userIdAlert(getUserId());
        }
    }).catch(error => console.error('Error:', error));
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