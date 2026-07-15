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

    if (document.getElementById("free-tier")) {
        initFreeTier();
        return;
    }

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

let freeKeyState = null;

function fmtCountdown(seconds) {
    if (seconds <= 0) return "expired";
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    return `${h}h ${m}m left`;
}

async function openLinkvertise() {
    const s = freeKeyState;
    if (!s || !s.publisher_id) {
        Swal.fire({ title: "Key system unavailable", text: "Please try again later." });
        return;
    }
    try {
        const res = await fetch("/api/key/challenge");
        if (!res.ok) throw new Error("challenge failed");
        const { target } = await res.json();
        const link = await window.linkvertiseLink(s.publisher_id, target);
        window.location.href = link;
    } catch (e) {
        Swal.fire({ title: "Could not open key link", text: "Please try again." });
    }
}

async function freeRefresh(btn) {
    if (btn) btn.disabled = true;
    const res = await fetch("/api/key/refresh", { method: "POST" });
    if (!res.ok) {
        if (btn) btn.disabled = false;
        Swal.fire({
            title: "No free refresh left",
            text: "Grab a new key to refresh your game again.",
        });
        return;
    }
    const data = await res.json();
    freeKeyState.game = data.game;
    freeKeyState.free_refreshes = data.free_refreshes;
    renderFreeTier();
}

function escapeHtml(str) {
    const d = document.createElement("div");
    d.textContent = str == null ? "" : String(str);
    return d.innerHTML;
}

function renderFreeTier() {
    const card = document.getElementById("free-tier-card");
    if (!card || !freeKeyState) return;
    const s = freeKeyState;
    const g = s.game || {};
    const locked = !s.valid;

    const thumb = g.thumbnail || "/assets/img/baseplate.webp";
    const name = escapeHtml(g.name || "Mystery Game");
    const creator = escapeHtml(g.creator || "Unknown");
    const description = escapeHtml(g.description || "").trim();

    const stat = (icon, value, label) => `
        <div class="ft-stat">
            <i class="bx ${icon}"></i>
            <div>
                <span class="ft-stat-value">${value.toLocaleString()}</span>
                <span class="ft-stat-label">${label}</span>
            </div>
        </div>`;

    let cta;
    if (locked) {
        cta = `
            <button class="ft-btn ft-btn-key" onclick="openLinkvertise()">
                <i class="bx bx-key"></i> Get 24h Key
            </button>
            <div class="ft-hint">Complete a quick link to unlock 24-hour access.</div>`;
    } else {
        const canRefresh = (s.free_refreshes || 0) > 0;
        const refreshBtn = canRefresh
            ? `<button class="ft-btn ft-btn-ghost" onclick="freeRefresh(this)">
                   <i class="bx bx-refresh"></i> Free Refresh
               </button>`
            : `<button class="ft-btn ft-btn-ghost" onclick="openLinkvertise()">
                   <i class="bx bx-key"></i> Get Key to Refresh
               </button>`;
        cta = `
            <button class="ft-btn ft-btn-play" onclick="window.location.href='roblox://experiences/start?placeId=${g.placeid}'">
                <i class="bx bx-play"></i> Play
            </button>
            <div class="ft-btn-row">
                <button class="ft-btn ft-btn-ghost" onclick="window.open('${g.url}')">
                    <i class="bx bx-link-external"></i> Page
                </button>
                ${refreshBtn}
            </div>
            <div class="ft-hint">
                <i class="bx bx-time"></i> ${fmtCountdown(s.seconds_left)}
                &middot; ${s.free_refreshes || 0} free refresh${(s.free_refreshes || 0) === 1 ? "" : "es"} left
            </div>`;
    }

    card.innerHTML = `
        <div class="ft-game ${locked ? "ft-locked" : ""}">
            <div class="ft-top">
                <div class="ft-media">
                    <img src="${thumb}" class="ft-thumb">
                    ${locked ? '<div class="ft-lock"><i class="bx bxs-lock-alt"></i><span>Locked</span></div>' : ""}
                </div>
                <div class="ft-info">
                    <h2 class="ft-title">${name}</h2>
                    <div class="ft-creator">By ${creator}</div>
                    <div class="ft-stats">
                        ${stat("bxs-star", g.favorites || 0, "Favorites")}
                        ${stat("bx-show", g.visits || 0, "Visits")}
                    </div>
                    <div class="ft-cta">${cta}</div>
                </div>
            </div>
            ${description ? `<div class="ft-about">
                <h3>About</h3>
                <div class="ft-desc">${description}</div>
            </div>` : ""}
        </div>`;
    animatePopulateItem(card.querySelector(".ft-game"));
}

async function initFreeTier() {
    try {
        const res = await fetch("/api/key/status");
        const data = await res.json();
        if (!data.free_tier) {
            // Whitelist changed mid-session; fall back to full grid.
            updateGames();
            return;
        }
        freeKeyState = data;
        renderFreeTier();
        const params = new URLSearchParams(window.location.search);
        if (params.get("key") === "success") {
            Swal.fire({ icon: "success", title: "Key activated!", text: "You have 24 hours of access." });
        } else if (params.get("key") === "failed") {
            Swal.fire({ icon: "error", title: "Verification failed", text: "Please complete the link without skipping." });
        }
    } catch (e) {
        const card = document.getElementById("free-tier-card");
        if (card) card.innerHTML = '<pre>Could not load your game. Please refresh.</pre>';
    }
}

updateGames();
