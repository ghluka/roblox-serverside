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
    const url = "/api/roblox_data?userid=" + getUserId();
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

function animatePopulateItems(container, selector) {
    if (!container) return;
    const items = Array.from(container.querySelectorAll(selector));
    items.forEach((item, index) => {
        item.classList.remove("populate-item");
        item.style.animationDelay = `${Math.min(index, 12) * 28}ms`;
        void item.offsetWidth;
        item.classList.add("populate-item");
    });
}

function updatePlayers() {
    const url = "/api/players";
    fetch(url, {
        method: "GET"
    }).then(response => response.text()).then(function(response) {
        const playerList = document.getElementById("player-list");
        playerList.innerHTML = response;
        animatePopulateItems(playerList, ".players");
        document.getElementById("playersearch").dispatchEvent(new Event("input"));
        const clientEl = document.getElementById('stat-client');
        const clientIconEl = document.getElementById('stat-client-icon');
        if (response == "") {
            document.getElementById("player-action-warning").innerHTML = `
            <h3>Waiting For Game...</h3>
            <br>
            <h5>To load the player list, your linked Roblox account must be in a whitelisted game.</h5>
            <h5>If you set your Roblox username in the dashboard while in-game, rejoin.</h5>
            `;
            document.getElementById("player-action-warning").style.display = "flex";
            document.getElementById("player-actions-container").style.display = "none";
            if (clientEl) { clientEl.textContent = 'Offline'; clientEl.className = 'stat-value stat-offline'; }
            if (clientIconEl) { clientIconEl.className = 'bx bx-wifi-off stat-icon stat-offline'; }
            return;
        }
        document.getElementById("player-action-warning").innerHTML = `
            <h3 class="found">Game Found!</h3>
            <br>
            <h5>Select a player on the left to see information and a list of scripts you can perform on them.</h5>
            `;
        if (clientEl) { clientEl.textContent = 'Online'; clientEl.className = 'stat-value stat-online'; }
        if (clientIconEl) { clientIconEl.className = 'bx bx-wifi stat-icon stat-online'; }
    }).catch(_ => { });
    document.getElementById("playersearch").dispatchEvent(new Event("input"));
    setTimeout(updatePlayers, 10000);
    document.getElementById("playersearch").dispatchEvent(new Event("input"));
}
updatePlayers();

function updateModules() {
    const url = "/api/modules";
    fetch(url, {
        method: "GET"
    }).then(response => response.text()).then(function(response) {
        const modules = document.getElementById("modules");
        modules.innerHTML = response;
        animatePopulateItems(modules, ".module");
    }).catch(error => console.error('Error:', error));
    setTimeout(updateModules, 60000 * 5);
}
updateModules();

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
    document.getElementById("walkspeed").value = data["WalkSpeed"];
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

function activateSwapGroup(group) {
    if (group.dataset.swapInit) return;
    group.dataset.swapInit = "true";
    const items = group.querySelectorAll('.swap-item');
    if (items.length === 0) return;
    let index = 0;
    items[index].classList.add('active');
    setInterval(() => {
        items[index].classList.remove('active');
        index = (index + 1) % items.length;
        items[index].classList.add('active');
    }, 5000);
}

document.querySelectorAll('.swap-group').forEach(activateSwapGroup);

const observer = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
        mutation.addedNodes.forEach(node => {
            if (node.classList && node.classList.contains('swap-group')) {
                activateSwapGroup(node);
            }
            if (node.querySelectorAll) {
                node.querySelectorAll('.swap-group').forEach(activateSwapGroup);
            }
        });
    });
});

observer.observe(document.body, { childList: true, subtree: true });

function initCustomSelect() {
    const customSelects = document.querySelectorAll('.custom-select');
    customSelects.forEach(container => {
        const select = container.querySelector('select');
        const selected = document.createElement('div');
        selected.className = 'select-selected';
        const firstOption = select.options[select.selectedIndex];
        if(firstOption.value){
            selected.innerHTML = `<img src="/api/decal?assetid=${firstOption.value}" alt=""> ${firstOption.text}`;
        } else {
            selected.innerHTML = firstOption.innerHTML + "<i class='bx bxs-chevron-down'></i>";
        }
        container.appendChild(selected);
        const optionsContainer = document.createElement('div');
        optionsContainer.className = 'select-items';
        Array.from(select.options).forEach(option => {
            if(option.value === "") return;
            const optionDiv = document.createElement('div');
            optionDiv.innerHTML = `<img src="/api/decal?assetid=${option.value}" alt=""> ${option.text}`;
            optionDiv.addEventListener('click', () => {
                select.value = option.value;
                selected.innerHTML = `<img src="/api/decal?assetid=${option.value}" alt=""> ${option.text} <i class='bx bxs-chevron-down'></i>`;
                optionsContainer.style.display = 'none';
                select.dispatchEvent(new Event('change'));
            });
            optionsContainer.appendChild(optionDiv);
        });
        container.appendChild(optionsContainer);
        selected.addEventListener('click', () => {
            if (selected.innerHTML.includes("bxs-chevron-down"))
                selected.innerHTML = selected.innerHTML.replace("bxs-chevron-down", "bxs-chevron-up");
            else
                selected.innerHTML = selected.innerHTML.replace("bxs-chevron-up", "bxs-chevron-down");
            optionsContainer.style.display = optionsContainer.style.display === 'flex' ? 'none' : 'flex';
        });
        document.addEventListener('click', e => {
            if(!container.contains(e.target)){
                selected.innerHTML = selected.innerHTML.replace("bxs-chevron-up", "bxs-chevron-down");
                optionsContainer.style.display = 'none';
            }
        });
    });
}

initCustomSelect();

// Seed scripts-executed stat from localStorage on page load
(function() {
    const count = parseInt(localStorage.getItem('nettss_executed') || '0');
    const el = document.getElementById('stat-scripts');
    if (el) el.textContent = count.toLocaleString();
}());

// Activity history feed
function historyIcon(type) {
    const icons = { signup: 'bxs-user-plus', whitelist: 'bxs-shield' };
    return icons[type] || 'bx-info-circle';
}

function formatHistoryTime(isoStr) {
    const d = new Date(isoStr + 'Z');
    const diff = Math.floor((Date.now() - d.getTime()) / 1000);
    if (diff < 60) return 'Just now';
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    if (diff < 2592000) return `${Math.floor(diff / 86400)}d ago`;
    return d.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
}

function loadHistory() {
    const list = document.getElementById('dash-history');
    if (!list) return;
    fetch('/api/history')
        .then(r => r.json())
        .then(events => {
            if (!events.length) {
                list.innerHTML = '<li class="dash-history-empty">No activity yet.</li>';
                return;
            }
            list.innerHTML = events.map(e => `
                <li class="dash-history-item dash-history-${e.event_type}">
                    <span class="dash-history-icon"><i class="bx ${historyIcon(e.event_type)}"></i></span>
                    <div>
                        <p class="dash-history-desc">${e.description}</p>
                        <span class="dash-history-time">${formatHistoryTime(e.timestamp)}</span>
                    </div>
                </li>
            `).join('');
        })
        .catch(() => {
            list.innerHTML = '<li class="dash-history-empty">Could not load history.</li>';
        });
}
loadHistory();
