import time
from pymongo import MongoClient

from utils import hash

"""A mongo database that maintains accounts, messages, and feed."""
client = MongoClient(host="mongo", port=27017)
db = client["database"]
accounts = db["accounts"]
messages = db["messages"]
feed = db["feed"]

# TODO Add unique ID for each account
def add_account(name, password):
    user_key = accounts.find_one({"name": name})
    if user_key is None:
        account = {
                "name": name,
                "password": password,
                "token": null
            }
        accounts.insert_one(account)
        return "Registration successful"
    else:
        return f"{name} already exists in database."

def changeAuthToken(user, token):
    accounts.find_one_and_update({"name": user}, {"$set":{"token": token}})


def fetch_account(name):
    return accounts.find_one({"name": name})


def fetch_account_by_id(id):
    return accounts.find_one({"id": id})


def fetch_account_by_token(token):
    hashed = hash(token)
    return accounts.find_one({"token": token})


def user_exists(id):
    return fetch_account_by_id(id) is not None


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


def add_feed(sender, post, caption):
    post = {
            "from": sender,
            "post": post,
            "caption": caption,
            "timestamp": time.time()
        }
    feed.insert_one(post)


def get_feed():
    return feed.find({})
