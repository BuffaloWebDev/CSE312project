import time
from pymongo import MongoClient

from utils import hash, escapeHTML

"""A mongo database that maintains accounts, messages, and feed."""
client = MongoClient(host="mongo", port=27017)
db = client["database"]
accounts = db["accounts"]
messages = db["messages"]
feed = db["feed"]
# feed.drop()
# accounts.drop()

# TODO Add unique ID for each account


def add_account(name, password):
    user_key = accounts.find_one({"name": name})
    if user_key is None:
        account = {
            "name": name,
            "password": password,
            "token": None,
            "greeting": "Hello there!"
        }
        accounts.insert_one(account)
        return "Registration successful"
    else:
        return f"{name} already exists in database."


def changeAuthToken(user, token):
    accounts.find_one_and_update({"name": user}, {"$set": {"token": token}})


def fetch_account(name):
    return accounts.find_one({"name": name})


def fetch_account_by_token(token):
    if isinstance(token, str):
        token = token.encode()

    print(token, flush=True)
    print(type(token), flush=True)
    hashed = hash(token)
    account = accounts.find_one({"token": hashed})
    if account is not None:
        return account["name"]


def fetch_accounts():
    return accounts.find({})


def add_message(sender, to, message):
    post = {
        "from": sender,
        "to": to,
        "message": message,
        "timestamp": time.time()
    }
    messages.insert_one(post)


def add_feed(sender, filename, caption):
    post = {
        "from": sender,
        "filename": filename,
        "caption": caption,
        "timestamp": time.time()
    }
    feed.insert_one(post)


def get_feed():
    return feed.find({})


def numberOfFeedItems():
    return len(list(get_feed()))


def changeGreeting(user, greeting):
    greeting = escapeHTML(greeting)
    accounts.find_one_and_update(
        {"name": user}, {"$set": {"greeting": greeting}})


def getGreeting(user):
    account = accounts.find_one({"name": user})
    if account is not None:
        return account["greeting"]
