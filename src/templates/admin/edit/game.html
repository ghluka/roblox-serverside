{% extends "app_base.html" %}
{% block title %}NettSS Game {{ game[0] }}{% endblock %}
{% block extra_css %}
    <style>html { overflow-y: scroll !important; }</style>
{% endblock %}
{% block body %}
    <div style="text-align: center;">
        <h1 onclick="window.location.href = '/admin'"><div class="logo_name"><span style="color: #bc49db;">Nett</span><span>SS</span></div></h1>
    </div>
    <div style="padding: 8px 16px !important; margin: 8px 16px !important; border: 2px solid #50407040; border-radius: 8px;">
        <h1>Editing Game {{ placeid }}</h1>

        <div id="gamePreview">
            <img id="gameThumb" src="">

            <div style="flex:1">
                <h2 id="gameTitle">Loading...</h2>
                <div id="gameData"></div>
                <div>
                    <button class="play-button" style="width: 350px;"
                        onclick="event.stopPropagation(); window.location.href=`roblox://experiences/start?placeId={{ placeid }}`">
                    <i class="bx bx-play"></i></button><br>
                    <button style="width: 350px;"
                        onclick="window.open('https://www.roblox.com/games/{{ placeid }}')">
                    <i class="bx bx-link-external"></i> Roblox Page</button>
                </div>
            </div>
        </div>

        <form method="POST" style="display: inline;">
            <label>Place ID</label><br>
            <input value="{{ game.placeid }}" disabled><br>
            
            <label>Whitelist</label><br>
            <input name="whitelist" value="{{ game.whitelist }}"><br>
            
            <button type="submit" style="background-color: var(--nett);">Save</button>
        </form>
        <button onclick="window.location.href = '/admin#gd'">Go back</button>
    </div>
    <script>
        fetch(`/api/game/{{ placeid }}`)
        .then(r => r.json())
        .then(data => {
        
            const g = data.data?.[0]
            if(!g) return
        
            document.getElementById("gameTitle").textContent = g.name
        
            document.getElementById("gameThumb").src =
                data.thumbnail || "/assets/img/baseplate.webp"
        
            document.getElementById("gameData").innerHTML =
                `by <b>${g.creator.name}</b> • ${g.visits} visits`
        
        })
        .catch(()=>{})
    </script>
{% endblock %}
