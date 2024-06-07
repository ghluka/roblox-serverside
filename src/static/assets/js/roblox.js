function getUsername() {
    const userid = document.getElementById("userid").value;
    const url = "https://users.roblox.com/v1/users/1" + userid
    fetch(url, {
        method: "GET"
    }).then(response => response.text()).then(function(response) {
            Swal.fire(response);
    }).catch(error => console.error('Error:', error));
}