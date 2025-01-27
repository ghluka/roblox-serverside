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

function FileInput(f) {
    let input = document.createElement('input');
    input.type = 'file';
    input.accept = '.lua,.txt';
    input.onchange = e => {
        var file = e.target.files[0];
        if (!file) {
            return;
        }
        var reader = new FileReader();
        reader.onload = function(e) {
            var contents = e.target.result;
            f(contents);
        };
        reader.readAsText(file);
    };
    return input
}

var SetFileInput = FileInput(contents => {
    SetText(contents);
})
function SetFile() {
    SetFileInput.click()
}

var ExecuteFileInput = FileInput(contents => {
    execute(contents);
})
function ExecuteFile() {
    ExecuteFileInput.click()
}

function SaveFile(contents) {
    const file = new File([contents], 'script.lua', {
        type: 'text/plain',
    })
    
    const link = document.createElement('a')
    const url = URL.createObjectURL(file)
    
    link.href = url
    link.download = file.name
    document.body.appendChild(link)
    link.click()
    
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
}

document.addEventListener('keydown', e => {
    if (e.ctrlKey) {
        if (e.key === 's') {
            e.preventDefault();
            SaveFile(GetText());
        }
        else if (e.key === 'o') {
            e.preventDefault();
            SetFile();
        }
    }
});

try {
    CefSharp.PostMessage("Close");
} catch (error) {}