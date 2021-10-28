document.addEventListener('DOMContentLoaded', () => {

    //Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    //Get user input and send to server
    document.getElementById("regButton").onclick = function() {
        var email = document.getElementById("regEmail").value;
        var username = document.getElementById("regUser").value;
        var password = document.getElementById("regPass").value;
        console.log(email, username, password);

        socket.emit("regData", {"email": email, "username": username, "password": password});
    };

    //If registration successful, redirect to homepage
    socket.on("regSuccess", data => {
        console.log("Emit recieved!");
        window.location.replace("/homepage");
    });

    //If registration unsuccessful due to email error, display an email error message
    socket.on("regErrorEmail", data => {
        console.log("Emit recieved!");
        let message = "Email already taken!";
        document.querySelector("#messageReg").innerHTML = message;
    });

    //If registration unsuccessful due to username error, display an username error message
    socket.on("regErrorUser", data => {
        console.log("Emit recieved!");
        let message = "Username already taken!";
        document.querySelector("#messageReg").innerHTML = message;
    });
});