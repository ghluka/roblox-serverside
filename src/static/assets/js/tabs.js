function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
  
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
  
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

const tabs = Array.from(document.getElementsByClassName("tablinks"));

const hash = location.hash.replace("#", "");
if (location.hash) {
    history.replaceState(null, "", location.pathname + location.search);
}

if (!hash) {
    tabs[0].click();
} else {
    const targetTab = tabs.find(btn => btn.getAttribute("onclick") === `openTab(event, '${hash}')`);

    if (targetTab) {
        targetTab.click();
    } else {
        tabs[0].click();
    }
}