# accounts.py

import parse
import database


def listUsers():
    return parse.encodeJSON(database.fetch_accounts())


def getUser(userID):
    return parse.encodeJSON(database.fetch_accounts_by_id(userID)) if database.user_exists(userID) else None


