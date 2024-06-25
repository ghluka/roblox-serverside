function userIdAlert(userid) {
    const url = "http://localhost:5000/api/roblox_data?userid=" + userid
    fetch(url, {
        method: "GET"
    }).then(response => response.json()).then(function(response) {
        if (response["error"]) {
            Swal.fire({
                title: response["error"]["error"],
                text: response["error"]["advice"],
            });
        }
        else {
            Swal.fire({
                title: "Unable to locate " + response["name"] + "!",
                text: "Please make sure you're in a game before executing a script.",
                imageUrl: response["avatarUrl"],
                imageWidth: 200,
                imageHeight: 200,
            });
        }
    }).catch(error => console.error('Error:', error));
}