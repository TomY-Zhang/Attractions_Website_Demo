document.addEventListener('DOMContentLoaded', () => {

    //Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    //Get user input and send to server
    document.getElementById("logButton").onclick = function() {
        var username = document.getElementById("logUser").value;
        var password = document.getElementById("logPass").value;
        console.log(username, password);

        socket.emit("checkCredentials", {"username": username, "password": password});
        console.log("Credentials successfully emitted to server!");
    };

    //If login succesful, redirect to homepage
    socket.on("loginSuccess", data => {
        console.log("Emit recieved!");
        window.location.replace("/homepage");
    });

    //If login unsuccessful, diplay an error message
    socket.on("loginError", data => {
        console.log("Emit recieved!");
        message = "Incorrect credentials";
        document.querySelector("#errorMessageLogin").innerHTML = message;
    });
});