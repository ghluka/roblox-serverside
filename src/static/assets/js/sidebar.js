let sidebar = document.querySelector(".sidebar");
let closeBtn = document.querySelector("#btn");
let searchBtn = document.querySelector(".bx-search");

closeBtn.addEventListener("click", () => {
    sidebar.classList.toggle("open");
    menuBtnChange();
})

function menuBtnChange() {
    if (sidebar.classList.contains("open")) {
        closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");
    } else {
        closeBtn.classList.replace("bx-menu-alt-right", "bx-menu");
    }
}

function openTab(evt, tabName) {
    var tabcontent = document.getElementsByClassName("home-section");
    if (evt)
        document.title = "NettSS " + evt.target.innerText;
    
    for (var i = 0; i < tabcontent.length; i++) {
        const tab = tabcontent[i];
        if (tab.id == tabName) {
            tabcontent[i].style.display = "flex";
            tab.classList.remove("tab-enter");
            void tab.offsetWidth;
            tab.classList.add("tab-enter");
        }
        else {
            tabcontent[i].style.display = "none";
            tab.classList.remove("tab-enter");
        }
    }

    if (evt) {
        var selected = document.getElementById("tab-selected");
        selected.id = "";
        if (evt.target.nodeName == "A")
            evt.target.id = "tab-selected";
        else
            evt.target.parentNode.id = "tab-selected";
    }
}

menuBtnChange();
closeBtn.click();
openTab(null, "dashboard")
