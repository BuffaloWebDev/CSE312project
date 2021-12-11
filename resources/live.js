socket = new WebSocket('ws://' + window.location.host + '/websocket');
socket.onmessage = parseMessage;

let current_user = document.getElementById('current-userName').value,
    redValue = document.getElementById("vr"),
    greenValue = document.getElementById("vg"),
    blueValue = document.getElementById("vb"),
    redSlider = document.getElementById("vrr"),
    greenSlider = document.getElementById("vgg"),
    blueSlider = document.getElementById("vbb");

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

function rgbToHex(r, g, b) {
    let hex = '#',
        red = r.toString(16),
        green = g.toString(16),
        blue = b.toString(16);
    if (red.length == 1) red = "0" + red;
    if (green.length == 1) green = "0" + green;
    if (blue.length == 1) blue = "0" + blue;
    return hex + red + green + blue;
};

function ca() {
    let r = redValue.innerHTML,
        g = greenValue.innerHTML,
        b = blueValue.innerHTML;
    socket.send(JSON.stringify({
        'from': current_user,
        'red': r,
        'green': g,
        'blue': b
    }));
};

function parseMessage(message) {
    const msgData = JSON.parse(message.data);
    let red = msgData["red"],
        green = msgData["green"],
        blue = msgData["blue"],
        color = rgbToHex(parseInt(red), parseInt(green), parseInt(blue));
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
