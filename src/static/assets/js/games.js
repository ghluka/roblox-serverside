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

function animatePopulateItem(item, index = 0) {
    if (!item) return;
    item.classList.remove("populate-item");
    item.style.animationDelay = `${Math.min(index, 12) * 28}ms`;
    void item.offsetWidth;
    item.classList.add("populate-item");
}

async function updateGames() {
    const url = "/api/games";
    const response = await fetch(url);
    const html = await response.text();

    let tc = "";
    if (document.getElementById("gamesearch")) {
        tc = document.getElementById("gamesearch").value;
    }

    document.getElementById("games_list").innerHTML = html;
    document.getElementById("gamesearch").value = tc;
    document.getElementById("gamesearch").dispatchEvent(new Event("input"));
    animatePopulateItems(document.getElementById("games_list"), ".game, .game-stats > div");

    let page = 0;
    let loading = false;
    let done = false;

    async function loadMore() {
        if (loading || done) return;
        loading = true;

        const res = await fetch(`/api/games/page?page=${page}`);

        if (document.getElementById("loadingGames")) {
            document.getElementById("loadingGames").remove();
        }
        const data = await res.json();

        if (data.games.length === 0) {
            done = true;
            loading = false;
            return;
        }

        for (const v of data.games) {
            try {
                const div = document.createElement("div");
                div.className = "game";
                div.onclick = () => window.open(v.url);

                div.innerHTML = `
                    <img src="${v.thumbnail}" class="preview-img">
                    <h3>${v.data[0].name}</h3>
                    <div class="swap-group">
                        <h5 class="swap-item"><i class='bx bxs-user'></i> ${v.data[0].visits.toLocaleString()} visits</h5>
                        <h5 class="swap-item"><i class='bx bxs-user'></i> ${v.data[0].playing.toLocaleString()} playing</h5>
                    </div>
                    <button class="play-button"
                        onclick="event.stopPropagation();
                        window.location.href='roblox://experiences/start?placeId=${v.placeid}'">
                        <i class="bx bx-play"></i>
                    </button>
                `;

                document.getElementById("games_list").appendChild(div);
                animatePopulateItem(div);
            }
            catch {}
        }

        page++;
        loading = false;
    }

    async function ensureScrollable() {
        const container = document.getElementById("games_list").parentNode;

        while (container.scrollHeight <= container.clientHeight && !done) {
            await loadMore();
            await new Promise(r => requestAnimationFrame(r));
        }
    }

    await loadMore();
    ensureScrollable();

    const parent = document.getElementById("games_list").parentNode;
    parent.addEventListener("scroll", () => {
        if (parent.scrollTop + parent.clientHeight >= parent.scrollHeight - 200) {
            loadMore();
        }
    });
}

updateGames();
