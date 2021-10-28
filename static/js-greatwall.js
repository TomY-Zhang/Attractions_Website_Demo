document.addEventListener('DOMContentLoaded', () => {

    //Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    //Send a message to the server as soon as the page loads
    socket.emit("gwPageLoaded");

    //Load all comments as soon as the page loads
    socket.on("gwLoadComments", data => {
        //Load all comments
        var comments = data['comments'];
        console.log("logging");
        console.log(comments);

        //Cycle through list of comments and add them to page 1 by 1
        for (var item in comments) {
            const li = document.createElement("li");
            li.innerHTML = comments[item];
            console.log("'li' text succesfully changed!");
            document.querySelector("#gwComment").append(li);
        }
    });

    //Send comment to the server
    var commentButton = document.getElementById("commentButton");
    commentButton.addEventListener("click", function() {
        var comment = document.getElementById("exampleFormControlTextarea1").value;
        console.log("Got comment from text area: " + comment);
        socket.emit("gwComment", {"comment": comment});
        console.log("Emit to server successful!");
    });

    //Append the comment to the comment section list
    socket.on("gwCommentAll", data => {
        const li = document.createElement("li");
        li.innerHTML = `${data.comment}`;
        console.log("Comment successfully received from server!");
        document.querySelector("#gwComment").append(li);
    });
});