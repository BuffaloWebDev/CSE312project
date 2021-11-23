# home.py

def serveHome(handler):
    with open("home.html") as f:
        responseBody = f.read()

    handler.sendMessage(responseBody, 200, "html")