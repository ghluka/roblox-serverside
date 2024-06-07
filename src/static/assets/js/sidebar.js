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
    var i, tabcontent;
    tabcontent = document.getElementsByClassName("home-section");
    for (i = 0; i < tabcontent.length; i++) {
        const tab = tabcontent[i];
        if (tab.id == tabName) {
            tabcontent[i].style.display = "block";
        }
        else {
            tabcontent[i].style.display = "none";
        }
    }
}

menuBtnChange();
openTab(null, "dashboard")