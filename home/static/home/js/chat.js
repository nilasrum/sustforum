$(function () {
    // Correctly decide between ws:// and wss://
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/chat/stream/";
    console.log("Connecting to " + ws_path);
    var socket = new ReconnectingWebSocket(ws_path);

    // Helpful debugging
    socket.onopen = function () {
        console.log("Connected to chat socket");
        var room_exist = $('#chat-room').length > 0;
        var roomId = $('#chat-room').attr('data-room-id');
        if (room_exist) {
            // Join room
            socket.send(JSON.stringify({
                "command": "join",
                "room": roomId
            }));
        }
    };
    socket.onclose = function () {
        console.log("Disconnected from chat socket");
    };

    socket.onmessage = function (message) {
        // Decode the JSON
        console.log("Got websocket message " + message.data);
        var data = JSON.parse(message.data);
        // Handle errors
        if (data.error) {
            alert(data.error);
            return;
        }
        // Handle joining
        if (data.join) {
            console.log("Joining room " + data.join);
            var roomdiv = $('#chat-room');
            roomdiv.find("#send").on("click", function () {
                var msg = roomdiv.find("#input").val();
                if($.trim(msg).length>0)
                    socket.send(JSON.stringify({
                        "command": "send",
                        "room": data.join,
                        "message": msg
                    }));
                roomdiv.find("#input").val("");
            });
            // Handle leaving
        } else if (data.leave) {
            console.log("Leaving room " + data.leave);
        } else if (data.message || data.msg_type != 0) {
            var msgdiv = $("#msgs-list");
            var ok_msg = "";
            // msg types are defined in chat/settings.py
            // Only for demo purposes is hardcoded, in production scenarios, consider call a service.
            switch (data.msg_type) {
                case 0:
                    // Message
                    ok_msg = "<li class='chat-msg'>" +
                        "<span class='chat-username'>" + data.username + " : </span>" +
                        "<span class='chat-body'>" + data.message + "</span>" +
                        "</li>";
                    break;
                case 1:
                    // Warning/Advice messages
                    ok_msg = "<li class='contextual-message text-warning'>" + data.message + "</li>";
                    break;
                case 2:
                    // Alert/Danger messages
                    ok_msg = "<li class='contextual-message text-danger'>" + data.message + "</li>";
                    break;
                case 3:
                    // "Muted" messages
                    ok_msg = "<li class='contextual-message text-muted'>" + data.message + "</li>";
                    break;
                case 4:
                    // User joined room
                    ok_msg = "<li class='contextual-message text-muted'>" + data.username + " joined the room!" + "</li>";
                    break;
                case 5:
                    // User left room
                    ok_msg = "<li class='contextual-message text-muted'>" + data.username + " left the room!" + "</li>";
                    break;
                default:
                    console.log("Unsupported message type!");
                    return;
            }
            msgdiv.append(ok_msg);
            $("#msgs").scrollTop(200);
        } else {
            console.log("Cannot handle message!");
        }
    };


    // Room join
    // $("document").ready(function () {
    //     var room_exist = $('#chat-room').length > 0;
    //     var roomId = $('#chat-room').attr('data-room-id');
    //     if (room_exist) {
    //         // Join room
    //         socket.send(JSON.stringify({
    //             "command": "join",
    //             "room": roomId
    //         }));
    //     }
    // });
});