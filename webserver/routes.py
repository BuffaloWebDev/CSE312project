import websocket
import database
import utils
import parse
import home
import accounts

from hashlib import sha256

files = ["style.css", "functions.js"]

redirects = {"/": "/login"}


def route(requestHeaders, requestBody, requestType, requestPath, handler):
    cookies = parse.cookies(requestHeaders["Cookie"]) if "Cookie" in requestHeaders else None

    if requestType == "GET":
        if requestPath == "/login":
            accounts.loginPage(handler)

        elif requestPath in redirects:
            handler.redirect(redirects[requestPath])

        elif requestPath == "/websocket" and "Upgrade" in requestHeaders[
            'Connection'] and "websocket" in requestHeaders['Upgrade']:
            randKey = requestHeaders['Sec-WebSocket-Key'][0]
            websocket.establish(handler, randKey)

        else:
            authToken = cookies.get(
                "auth-token") if cookies is not None and "auth-token" in cookies else None

            if not accounts.checkAuthToken(authToken):
                handler.denied()

            if requestPath == "/home":
                home.serveHome(handler)

            elif requestPath == "/newPost":
                home.newPostPage(handler)

            elif requestPath == "/dm":
                home.dmPage(handler, authToken)

            elif requestPath[1:] in files:  # public files
                with open(f"resources{requestPath}", "rb") as requestedFile:
                    responseBody = requestedFile.read()
                extension = requestPath[1:].split(".")[-1]
                handler.sendMessage(responseBody, extension)

            else:
                uploadedImages = [item["filename"] for item in database.get_feed()]

                if requestPath[1:] in uploadedImages:
                    with open(f"resources/uploadedImages{requestPath}", "rb") as f:
                        responseBody = f.read()
                    handler.sendMessage(responseBody, "jpg")

                handler.notFound()

        # TODO Add routes for each page in the website with their own .py files (keep it modular)



    elif requestType == "POST":
        if requestPath == "/users":
            requestBody = parse.decodeJSON(requestBody)
            # TODO Update args
            responseBody = parse.encodeJSON(database.add_account())
            handler.sendMessage(responseBody, 201, "js")

        else:
            length = int(requestHeaders['Content-Length'][0])
            delimiter = b"--" + bytes(requestHeaders['Content-Type'][1][10:], encoding="utf-8")
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

                    database.changeAuthToken(username, token)
                    responseHeaders = [utils.cType["plain"], utils.nosniff,
                                       utils.contentLength(len(responseBody))]
                    responseHeaders.append(
                        utils.setCookie("auth-token", token, ["Max-Age = 3600", "HttpOnly"]))

                    accounts.addOnlineUser(username, handler)

                    handler.stitch(200, responseHeaders, responseBody)
                    # handler.redirect("/home")
                else:
                    handler.sendMessage(responseBody)
            elif requestPath == "/newPost":
                home.newPostSubmission(handler, cookies, form)

    elif requestType == "PUT":
        if requestPath[:7] == "/users/":
            userID = requestPath[7:]
            form = parse.decodeJSON(requestBody)

            if database.userExists(userID):
                # TODO Add args to database.update_account()
                updatedUser = database.update_account()
                handler.sendMessage(parse.encodeJSON(updatedUser), 200, "js")
            else:
                handler.notFound()

    # TODO Implement in database
    elif requestType == "DELETE":
        if requestPath[:7] == "/users/":
            userID = requestPath[7:]

            if database.user_exists(userID):
                # database.removeUser(userID)
                handler.stitch([utils.status[204]])
            else:
                handler.notFound()
        else:
            print("Error, request type not recognized")
