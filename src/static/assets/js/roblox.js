function userIdAlert(userid) {
    const url = "http://localhost:5000/api/roblox_data?userid=" + userid
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
    var userid = document.getElementById("userid").value;
    const url = "http://localhost:5000/api/roblox_data?userid=" + userid;
    fetch(url, {
        method: "GET"
    }).then(response => response.json()).then(function(response) {
        if (!response["error"]) {
            document.getElementById("username").innerHTML = response["name"];
            document.getElementById("avatar").src = response["avatarUrl"];
        }
    }).catch(error => console.error('Error:', error));
}
function updateUserDashboard() {
    var userid = document.getElementById("userid").value;
    setCookie("userid", userid, 30);
    updateUserInfoDashboard();
}
let user = getCookie("userid");
if (user != "") {
    document.getElementById("userid").value = user;
}
updateUserInfoDashboard();