socket = new WebSocket('ws://' + window.location.host + '/websocket');
socket.onmessage = parseMessage;
let current_user = document.getElementById('current-userName').value;

let redValue =  document.getElementById("vr")
let greenValue = document.getElementById("vg")
let blueValue = document.getElementById("vb")

let redSlider = document.getElementById("vrr")
let greenSlider = document.getElementById("vgg")
let blueSlider = document.getElementById("vbb")

function cr(value) {
    redValue.innerHTML = value;
    ca();
    };

function cg(value) {
    greenValue.innerHTML = value;
    ca();
};

function cb(value) {
    blueValue.innerHTML = value;
    ca();
};

function rgbToHex(r, g, b){
    let hex = '#';

    let red = r.toString(16);
    if(red.length == 1) {
        red = "0" + red;
    }
    let green = g.toString(16);
    if(green.length == 1) {
            green = "0" + green;
        }
    let blue = b.toString(16);
    if(blue.length == 1) {
            blue = "0" + blue;
        }

    return hex + red + green + blue;
}

function ca() {
    let r = redValue.innerHTML;
    let g = greenValue.innerHTML;
    let b = blueValue.innerHTML;
    socket.send(JSON.stringify({
        'from': current_user,
        'red': r,
        'green': g,
        'blue': b
    }));
};

function parseMessage(message) {
    const msgData = JSON.parse(message.data);

    let red = msgData["red"];
    let green = msgData["green"];
    let blue = msgData["blue"];

    let color = rgbToHex(parseInt(red), parseInt(green), parseInt(blue));
    console.log(color);
    document.body.style.backgroundColor = "rgb(" + red + "," + green + "," + blue + ")";

    redValue.innerHtml = red;
    greenValue.innerHtml = green;
    blueValue.innerHtml = blue;

    redSlider.value = red;
    greenSlider.value = green;
    blueSlider.value = blue;

    document.getElementById("announce").innerHTML = "Color: " + color;
    document.getElementById("picked-by").innerHTML = "Picked by: " + msgData["from"];
};
