const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

function execute(script) {
    const userid = document.getElementById("userid").value;
    const url = window.location.origin + "/api/execute?userid=" + userid
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "text/plain"
        },
        body: script
    }).then(response => response.text()).then(function(response) {
        if (response == "NO CLIENT") {
            Swal.fire("No client!", "Unable to find user " + userid + ".");
        }
    }).catch(error => console.error('Error:', error));
}

function executeRequire(script, user)
{
    execute("local username = \"" + user + "\"\n" + script);
}
