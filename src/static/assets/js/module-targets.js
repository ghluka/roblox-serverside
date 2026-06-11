(function () {
    const state = {
        all: false,
        selected: new Set(),
        players: []
    };

    const picker = document.getElementById("module-target-picker");
    const button = document.getElementById("module-target-button");
    const label = document.getElementById("module-target-label");
    const menu = document.getElementById("module-target-menu");
    const allInput = document.getElementById("module-target-all");
    const options = document.getElementById("module-target-options");

    if (!picker || !button || !label || !menu || !allInput || !options) return;

    function renderLabel() {
        if (state.all) {
            label.textContent = state.players.length ? `All players (${state.players.length})` : "All players";
            return;
        }

        const count = state.selected.size;
        if (count === 0) {
            label.textContent = "Linked player";
        } else if (count === 1) {
            const username = Array.from(state.selected)[0];
            const player = state.players.find(p => p.username === username);
            label.textContent = player?.displayName || username;
        } else {
            label.textContent = `${count} players`;
        }
    }

    function renderOptions() {
        allInput.checked = state.all;
        options.innerHTML = "";

        if (state.players.length === 0) {
            options.innerHTML = '<p class="target-empty">Waiting for players...</p>';
            renderLabel();
            return;
        }

        state.players.forEach(player => {
            const option = document.createElement("label");
            option.className = "target-option";
            option.innerHTML = `
                <input type="checkbox" value="${player.username}">
                <span>
                    <strong>${player.displayName || player.username}</strong>
                    <small>@${player.username}</small>
                </span>
            `;

            const input = option.querySelector("input");
            input.checked = state.all || state.selected.has(player.username);
            input.disabled = state.all;
            input.addEventListener("change", () => {
                if (input.checked) {
                    state.selected.add(player.username);
                } else {
                    state.selected.delete(player.username);
                }
                renderLabel();
            });

            options.appendChild(option);
        });

        renderLabel();
    }

    async function refreshTargets() {
        try {
            const response = await fetch("/api/players.json");
            const data = await response.json();
            const players = Array.isArray(data.players) ? data.players : [];
            const usernames = new Set(players.map(player => player.username));

            state.players = players;
            state.selected.forEach(username => {
                if (!usernames.has(username)) state.selected.delete(username);
            });

            renderOptions();
        } catch (_) {
            renderOptions();
        }
    }

    allInput.addEventListener("change", () => {
        state.all = allInput.checked;
        renderOptions();
    });

    button.addEventListener("click", () => {
        const open = picker.classList.toggle("open");
        button.setAttribute("aria-expanded", open ? "true" : "false");
    });

    document.addEventListener("click", event => {
        if (!picker.contains(event.target)) {
            picker.classList.remove("open");
            button.setAttribute("aria-expanded", "false");
        }
    });

    window.getModuleTargets = function () {
        if (state.all) {
            return state.players.map(player => player.username);
        }

        return Array.from(state.selected);
    };

    renderLabel();
    refreshTargets();
    setInterval(refreshTargets, 10000);
}());
