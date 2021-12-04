# accounts.py

import parse
import database
import utils

from bcrypt import hashpw, checkpw, gensalt

def loginPage(handler):
    with open("login.html") as f:
        responseBody = f.read().encode()

    xsrf = utils.token().encode()
    utils.addToken(xsrf)

    replacements = [(b"{{XSRFToken}}", xsrf)]
    utils.template(responseBody, replacements)
    responseBody = responseBody.replace(b"{{XSRFToken}}", xsrf)

    handler.sendMessage(responseBody, "html", 200)

# TODO Add pwd requirements
def validPassword(pwd):
    return True

def login(username, pwd):
    credentials = database.fetch_account(username)
    if credentials is None:
        return "Login failed"
    pwd = pwd.decode().encode("UTF-8")
    hashed = credentials["password"]

    return "Login Failed" if hashed is None or not checkpw(pwd, hashed) else "You logged in"


def register(username, pwd):
    if validPassword(pwd):
        hashed = hashpw(pwd, gensalt())
        return database.add_account(username, hashed)
    return "Password must meet all requirements"

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