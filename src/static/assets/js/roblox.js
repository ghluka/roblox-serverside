function getUserId() {
    if (document.getElementById("userid"))
        return document.getElementById("userid").value
    return "1";
}

function userIdAlert(userid) {
    const url = "/api/roblox_data?userid=" + userid
    fetch(url, {
        method: "GET"
    }).then(response => response.json()).then(function(response) {
        if (response["error"]) {
            Swal.fire({
                title: response["error"]["error"],
                text: response["error"]["advice"],
            });
        }
        else {
            Swal.fire({
                title: "Unable to locate " + response["name"] + "!",
                text: "Please make sure you're in a game before executing a script.",
                imageUrl: response["avatarUrl"],
                imageWidth: 200,
                imageHeight: 200,
            });
        }
    }).catch(error => console.error('Error:', error));
}

function setCookie(cname,cvalue,exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
  
function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
}

function updateUserInfoDashboard() {
    var userid = getUserId()
    const url = "/api/roblox_data?userid=" + userid;
    fetch(url, {
        method: "GET"
    }).then(response => response.json()).then(function(response) {
        if (!response["error"]) {
            document.getElementById("username").innerHTML = response["name"];
            document.querySelectorAll('[id="avatar"]').forEach(el => {
                el.src = response["avatarUrl"];
            });
        }
    }).catch(error => console.error('Error:', error));
}
//let user = getCookie("userid");
//if (user != "") {
//    document.getElementById("userid").value = user;
//}
updateUserInfoDashboard();

function updatePlayers() {
    var userid = getUserId()
    const url = "/api/players?userid=" + userid;
    fetch(url, {
        method: "GET"
    }).then(response => response.text()).then(function(response) {
        document.getElementById("player-list").innerHTML = response;
        if (response == "") {
            document.getElementById("player-action-warning").innerHTML = `
            <h3>Waiting For Game...</h3>
            <br>
            <h5>To load the player list, your linked Roblox account must be in a whitelisted game.</h5>
            <h5>If you set your Roblox Id in the dashboard while in-game, rejoin.</h5>
            `;
            document.getElementById("player-action-warning").style.display = "flex";
            document.getElementById("player-actions-container").style.display = "none";
            return;
        }
        document.getElementById("player-action-warning").innerHTML = `
            <h3 class="found">Game Found!</h3>
            <br>
            <h5>Select a player on the left to see information and a list of scripts you can perform on them.</h5>
            `;
    }).catch(_ => { });
    setTimeout(updatePlayers, 10000);
}
updatePlayers();

function updateModules() {
    const url = "/api/modules";
    fetch(url, {
        method: "GET"
    }).then(response => response.text()).then(function(response) {
        document.getElementById("modules").innerHTML = response;
    }).catch(error => console.error('Error:', error));
    setTimeout(updateModules, 60000);
}
updateModules();

function updateGames() {
    const url = "/api/games";
    fetch(url, {
        method: "GET"
    }).then(response => response.text()).then(function(response) {
        document.getElementById("games_list").innerHTML = response;
    }).catch(error => console.error('Error:', error));
    setTimeout(updateGames, 60000);
}
updateGames();

function getFlagEmoji(countryCode) {
    const codePoints = countryCode.toUpperCase().split('').map(char =>  127397 + char.charCodeAt());
    return String.fromCodePoint(...codePoints);
  }

function setPlayer(event) {
    var dataNode = event.target;
    while (dataNode.nodeName !== "A") {
        dataNode = dataNode.parentNode;
    }
    document.getElementById("player-action-warning").style.display = "none";
    var data = JSON.parse(dataNode.getAttribute("data").replaceAll("'", "\""));
    document.getElementById("player-action-avatar").src = data["AvatarUrl"];
    document.getElementById("player-action-displayname").innerHTML = data["DisplayName"] + twemoji.parse(getFlagEmoji(data["Country"]));
    document.getElementById("player-action-username").innerHTML = "@" + data["Username"];
    document.getElementById("player-actions").setAttribute("userid", data["UserId"]);
    document.getElementById("player-actions-container").style.display = "flex";
}
document.getElementById("player-actions-container").style.display = "none";

function resetRobloxId() {
    const url = "/api/update_id?userid=1";
    fetch(url, {
        method: "GET"
    }).then((_) => {
        location.reload();
    })
}

async function robloxUsernameToId(username) {
    const res = await fetch("/api/roblox-user-id", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username })
    });
    const data = await res.json();
    return data?.data?.[0]?.id ?? 1;
}
