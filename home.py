# home.py

def serveHome(handler):
    with open("home.html") as f:
        responseBody = f.read()

    handler.sendMessage(responseBody, "html", 200)