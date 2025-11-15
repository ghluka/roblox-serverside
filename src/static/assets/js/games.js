
function updateGames() {
    const url = "/api/games";
    fetch(url, {
        method: "GET"
    }).then(response => response.text()).then(function(response) {
        let tc = "";
        if (document.getElementById("gamesearch")) {
            tc = document.getElementById("gamesearch").value;
            console.log(tc);
        }
        document.getElementById("games_list").innerHTML = response;
        document.getElementById("gamesearch").value = tc;
        document.getElementById("gamesearch").dispatchEvent(new Event("input"));

        let page = 0;
        let loading = false;
        let done = false;

        async function loadMore() {
            if (loading || done) return;
            loading = true;
        
            const res = await fetch(`/api/games/page?page=${page}`);
            const data = await res.json();
        
            if (data.games.length === 0) {
                done = true;
                return;
            }
        
            data.games.forEach(v => {
                const div = document.createElement('div');
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
                    </button>`;

                document.getElementById("games_list").appendChild(div);
                if (document.getElementById("loadingGames")) {
                    document.getElementById("loadingGames").remove()
                }
            });
        
            page++;
            loading = false;
        }

        loadMore();

        document.getElementById("games").children[0].addEventListener("scroll", () => {
            if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 200) {
                loadMore();
            }
        });
    }).catch(error => console.error('Error:', error));
}
updateGames();
