# accounts.py

import parse
import database
import utils


from bcrypt import hashpw, checkpw, gensalt

def loginPage(handler):
    with open("resources/login.html", "rb") as f:
        responseBody = f.read()

    xsrf = utils.token().encode()
    utils.addToken(xsrf)

    replacements = [(b"{{XSRFToken}}", xsrf)]
    utils.template(responseBody, replacements)
    responseBody = responseBody.replace(b"{{XSRFToken}}", xsrf)

    handler.sendMessage(responseBody, "html", 200)

def validUsername(username):
    return not any([str(char) in "<>&/" for char in username])

def validPassword(pwd):
    pwd = pwd.decode()
    longEnough = (len(pwd) >= 8)
    notPwd = (pwd != "password")
    lowercase = any([str(char).islower for char in pwd])
    uppercase = any([str(char).isupper for char in pwd])
    containsNum = any([str(char).isdigit for char in pwd])
    containsSpecial = any([str(char) in "`~!@#$%^*()-_=+[{]}\|;:,.?" for char in pwd])
    html = not any([str(char) in "<>&/" for char in pwd])
    return longEnough and notPwd and lowercase and uppercase and containsNum and containsSpecial and html

def login(username, pwd):
    credentials = database.fetch_account(username)
    if credentials is None:
        return "Login failed"
    pwd = pwd.decode().encode("UTF-8")
    hashed = credentials["password"]

    return "Login Failed" if hashed is None or not checkpw(pwd, hashed) else "You logged in"


def register(username, pwd):
    if validPassword(pwd) and validUsername(username):
        hashed = hashpw(pwd, gensalt())
        return database.add_account(username, hashed)
    return "Username and password must meet all requirements"

def listUsers():
    return parse.encodeJSON(database.fetch_accounts())

def getUser(userID):
    return parse.encodeJSON(database.fetch_accounts_by_id(userID)) if database.user_exists(userID) else None

# Checks if a user is logged in, given an auth token
def checkAuthToken(token):
    if token is None:
        return False

    user = database.fetch_account_by_token(token)
    return user is not None


clients = []


def getOnlineUsers():
    return clients

def getUserByHandler(handler):
    for client in clients:
        if client["handler"] == handler:
            return client

def addOnlineUser(username, handler):
    clients.append({
        "username": username,
        "handler": handler
    })

def removeOnlineUser(handler):
    global clients
    clients = [client for client in clients if client["handler"] != handler]

