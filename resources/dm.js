socket = new WebSocket('ws://' + window.location.host + '/websocket');
socket.onmessage = parseMessage;

let current_user = document.getElementById("current-userName").value;


function sendMsg() {
    let message_box = document.getElementById("text-msg");
    let picked_user = document.getElementById("dm-people").value;
    let msg_value = message_box.value;
    if (picked_user !== '' && msg_value !== '' && current_user !== '') {
        socket.send(JSON.stringify({
            'from': current_user,
            'to': picked_user,
            'msg': msg_value
        }));
        message_box.value == "";
    }
}

function replyMsg(from) {
    let message_box = document.getElementById("reply-msg");
    let msg_value = message_box.value;
    if (from !== '' && msg_value !== '' && current_user !== '') {
        socket.send(JSON.stringify({
            'from': current_user,
            'to': from,
            'msg': msg_value
        }));
        document.getElementById("reply-section").innerHTML = "";
    }
}

function parseMessage(message) {
    const msgData = JSON.parse(message.data);
    console.log(msgData);
    if (msgData['to'] == current_user) {
        document.getElementById("reply-section").innerHTML = (
        "<p>" + msgData["from"] + ":" + msgData["msg"] + "</p>" +
        "<input type='text' id='reply-msg'>" +
        "<button id='reply-msg' onclick='replyMsg(\"" + msgData["from"] + "\")'> Reply </button>"
        );
    }
}