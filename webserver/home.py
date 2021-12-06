# home.py

from accounts import getOnlineUsers, checkAuthToken
from utils import template, token, addToken
from database import get_feed, add_feed, numberOfFeedItems, fetch_account_by_token

def serveHome(handler):
    with open("resources/home.html", "rb") as f:
        responseBody = f.read()

    clients = getOnlineUsers()

    clientListHTML = ""
    for client in clients:
        clientListHTML += f"{client['username']} <br/>"

    feedHTML = ""
    feed = get_feed()
    for item in feed:
        feedHTML += f"<div class = feedItem> " \
                        f"""<img src = '{item["filename"]}' width ='800'> <br/>""" \
                        f"<p>{item['from']}: {item['caption'].decode()}</p>" \
                    f"</div> <br/>"

    replacements = [("{{OnlineUsers}}", clientListHTML), ("{{Feed}}", feedHTML)]
    responseBody = template(responseBody, replacements)

    handler.sendMessage(responseBody, "html", 200)

def newPostPage(handler):
    with open(f"resources/newPost.html", "rb") as requestedFile:
        responseBody = requestedFile.read()

    xsrf = token().encode()
    addToken(xsrf)
    responseBody = responseBody.replace(b"{{XSRFToken}}", xsrf)

    handler.sendMessage(responseBody, "html")

def dmPage(handler, authToken):
    if not checkAuthToken(authToken):
        print("Auth token broken", flush=True)
        handler.denied()

    username = fetch_account_by_token(authToken)

    with open(f"resources/dm.html", "rb") as requestedFile:
        responseBody = requestedFile.read()

    clients = getOnlineUsers()
    clientListHTML = ""
    for client in clients:
        clientListHTML += f'<option value="{client["username"]}">{client["username"]}</option>'
    
    replacements = [("{{OnlineUsers}}", clientListHTML), ("{{userName}}", username)]
    responseBody = template(responseBody, replacements)

    handler.sendMessage(responseBody, "html")

def newPostSubmission(handler, cookies, form):
    authToken = cookies.get("auth-token") if cookies is not None and "auth-token" in cookies else None

    if not checkAuthToken(authToken):
        print("Auth token broken", flush=True)
        handler.denied()

    username = fetch_account_by_token(authToken)

    image = form.get("image")
    number = numberOfFeedItems()
    filename = f"image{number}.jpg"
    with open(f"resources/uploadedImages/{filename}", "wb") as f:
        f.write(image)

    caption = form.get("caption")
    add_feed(username, filename, caption)

    handler.redirect("/home")


