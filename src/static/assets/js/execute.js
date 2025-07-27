const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

function execute(script) {
    const userid = document.getElementById("userid").value;
    const url = window.location.origin + "/api/execute?userid=" + userid;

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "text/plain"
        },
        body: script
    }).then(response => response.text()).then(function(response) {
        if (response == "NO CLIENT") {
            userIdAlert(userid);
        }
    }).catch(error => console.error('Error:', error));
}

function executeSS(script) {
    const userid = document.getElementById("userid").value;
    const url = window.location.origin + "/api/execute_ss?userid=" + userid;
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "text/plain"
        },
        body: script
    }).then(response => response.text()).then(function(response) {
        if (response == "NO CLIENT") {
            userIdAlert(userid);
        }
    }).catch(error => console.error('Error:', error));
}

function executeRequire(script)
{
    const userid = document.getElementById("userid").value;
    var username =  document.getElementById("module-username").value;
    if (username == "") {
        var username = document.getElementById("username").innerHTML;
    }
    const url = window.location.origin + "/api/execute_module?userid="+ userid + "&username=" + username
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "text/plain"
        },
        body: script
    }).then(response => response.text()).then(function(response) {
        if (response == "NO CLIENT") {
            userIdAlert(userid);
        }
    }).catch(error => console.error('Error:', error));
}

function executePlayerAction(script) {
    const userid = document.getElementById("userid").value;
    const targetid = document.getElementById("player-actions").getAttribute("userid");
    
    script = "local targethum = targetchar:FindFirstChildOfClass('Humanoid')\n" + script
    script = "local targetchar = target.Character\n" + script
    script = "local target = game:GetService('Players'):GetPlayerByUserId(" + targetid + ")\n" + script
    script = "local plrchar = plr.Character\n" + script
    script = "local plr = game:GetService('Players'):GetPlayerByUserId(" + userid + ")\n" + script
    
    executeSS(script);
}