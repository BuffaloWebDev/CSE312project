import websocket
import database
import utils
import parse
import home
import accounts

# HTTP Status codes
status = {101: "101 Switching Protocols",
          200: "200 OK",
          201: "201 Created",
          204: "204 No Content",
          301: "301 Moved Permanently",
          304: "Not Modified",
          403: "403 Forbidden",
          404: "404 Not Found",
          500: "500 Internal Server Error"}

# MIME content types
cType = {"plain": "Content-Type: text/plain;charset=UTF-8",
         "txt": "Content-Type: text/plain;charset=UTF-8",
         "html": "Content-Type: text/html;charset=UTF-8",
         "css": "Content-Type: text/css;charset=UTF-8",
         "js": "Content-Type: text/javascript;charset=UTF-8",
         "png": "Content-Type: image/png",
         "jpg": "Content-Type: image/jpeg",
         "jpeg": "Content-Type: image/jpeg",
         "mp4": "Content-Type: video/mp4"}

nosniff = "X-Content-Type-Options: nosniff"


def route(requestHeaders, requestBody, requestType, requestPath, handler):

    if requestType == "GET":
        if requestPath == "/":
            home.serveHome(handler)

        elif requestPath == "/websocket" and "Upgrade" in requestHeaders['Connection'] and "websocket" in requestHeaders['Upgrade']:
            randKey = requestHeaders['Sec-WebSocket-Key'][0]
            websocket.establish(handler, randKey)

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
