import websocket
import database
import utils
import parse
import home
import accounts

files = ["style.css", "functions.js"]


def route(requestHeaders, requestBody, requestType, requestPath, handler):

    if requestType == "GET":
        if requestPath == "/":
            home.serveHome(handler)

        elif requestPath == "/websocket" and "Upgrade" in requestHeaders['Connection'] and "websocket" in requestHeaders['Upgrade']:
            randKey = requestHeaders['Sec-WebSocket-Key'][0]
            websocket.establish(handler, randKey)

        elif requestPath[1:] in files:  # public files
            with open(requestPath[1:], "rb") as requestedFile:
                responseBody = requestedFile.read()
            extension = requestPath[1:].split(".")[-1]
            handler.sendMessage(responseBody, 200, extension)


        # TODO Add routes for each page in the website with their own .py files (keep it modular)

        else:
            handler.notFound()

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

            if not index.tokenCheck(token):
                handler.denied()

            elif requestPath == "/comment":
                username = utils.escapeHTML(form['name'])
                submission = utils.escapeHTML(form['comment'])

                index.addComment({"name": username, "comment": submission})
                handler.redirect("/")

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
                #database.removeUser(userID)
                handler.stitch([status[204]])
            else:
                handler.notFound()
        else:
            print("Error, request type not recognized")
