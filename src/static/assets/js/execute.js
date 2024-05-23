const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const userid = document.getElementById("userid").value;

function execute(script) {
    const url = window.location.origin + "/api/execute?userid=" + userid
    console.log(script);
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "text/plain"
        },
        body: script
    }).then(response => response.text()).then(function(response) {
        if (response == "NO CLIENT") {
            Swal.fire("No client!");
        }
    }).catch(error => console.error('Error:', error));
}