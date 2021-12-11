import websocket
import database
import utils
import parse
import home
import accounts

redirects = {"/": "/login"}

files = ["/style.css", "/live.js", "/dm.js"]


def route(requestHeaders, requestBody, requestType, requestPath, handler):
    cookies = parse.cookies(requestHeaders.get("Cookie"))

    if requestType == "GET":
        if requestPath == "/login":
            accounts.loginPage(handler)

        elif requestPath in redirects:
            handler.redirect(redirects[requestPath])

        elif requestPath == "/websocket" and "Upgrade" in requestHeaders['Connection'] and "websocket" in requestHeaders['Upgrade']:
            randKey = requestHeaders['Sec-WebSocket-Key'][0]
            websocket.establish(handler, randKey)

        elif requestPath in files:  # Public files (css and js)
            with open(f"resources{requestPath}", "rb") as requestedFile:
                responseBody = requestedFile.read()
            extension = requestPath.split(".")[-1]
            handler.sendMessage(responseBody, extension)

        else:
            authToken = cookies.get(
                "auth-token") if cookies is not None and "auth-token" in cookies else None

            if not accounts.checkAuthToken(authToken):
                handler.redirect("/login")

            if requestPath == "/home":
                home.serveHome(handler, authToken)

            elif requestPath == "/newPost":
                home.newPostPage(handler)

            elif requestPath == "/dm":
                home.dmPage(handler, authToken)

            elif requestPath == "/live":
                home.livePage(handler, authToken)

            else:
                uploadedImages = [item["filename"]
                                  for item in database.get_feed()]

                if requestPath[1:] in uploadedImages:
                    with open(f"resources/uploadedImages{requestPath}", "rb") as f:
                        responseBody = f.read()
                    handler.sendMessage(responseBody, "jpg")

                handler.notFound()

    elif requestType == "POST":
        if requestPath == "/users":
            pass

        else:
            length = int(requestHeaders['Content-Length'][0])
            delimiter = b"--" + \
                bytes(requestHeaders['Content-Type'][1][10:], encoding="utf-8")
            while len(requestBody) < length:
                requestBody += handler.request.recv(2048)

            form = parse.form(requestBody, delimiter)

            token = form.get('xsrf_token')
            if not utils.tokenCheck(token):
                handler.denied()
                return

            if requestPath == "/login" or requestPath == "/register":
                username = form.get("username").decode()
                pwd = form.get("password")

                responseBody = accounts.login(username, pwd) if requestPath == "/login" \
                    else accounts.register(username, pwd)

                if responseBody == "You logged in":
                    token = utils.token()
                    hashed = utils.hash(token)

                    database.changeAuthToken(username, hashed)

                    responseHeaders = [utils.setCookie(
                        "auth-token", token, ["Max-Age = 3600", "HttpOnly"])]

                    accounts.addOnlineUser(username, handler)
                    handler.redirect("/home", responseHeaders)
                else:
                    handler.sendMessage(responseBody)
            elif requestPath == "/newPost":
                authToken = cookies.get("auth-token") \
                    if cookies is not None and "auth-token" in cookies else None

                home.newPostSubmission(handler, authToken, form)
            elif requestPath == "/greeting":
                authToken = cookies.get("auth-token") \
                    if cookies is not None and "auth-token" in cookies else None

                username = database.fetch_account_by_token(authToken)
                greeting = form.get("greeting")
                if greeting is not None and username is not None:
                    database.changeGreeting(username, greeting)
                handler.redirect("/home")

    else:
        print("Error, request type not recognized")
