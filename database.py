import time
from pymongo import MongoClient


# """Today's meeting will be pretty casual and short. As for what I have for everyone:
# -Let's get started on our individual tasks. It's better to at least have something basic now so we're not trying to make the HTML and stuff while figuring our the more complex parts.
# -Home page: Definitely needs websocket connections for live interactions. I can get that working but I won't push that to the repo until HW3 is done. Also needs database to host the feed
# -Login: Need database connection to save accounts
# -DM: Probably needs websockets to do notifications/update chat. Same with database to save messages, at least until the recipient sees it.
# -Database: As we can see, everything else requires a functioning database. So that should get done ASAP so we can develop the rest of the project."""
class Database(object):
    """A mongo database that maintains accounts, messages, and feed."""

    def __init__(self):
        mongoURL = "" # mongodb://mongo_url
        client = MongoClient(mongoURL)
        db = client["database"]
        self.accounts = db["accounts"]
        self.messages = db["messages"]
        self.feed = db["feed"]

    def add_account(self, name, password):
        user_key = self.accounts.find_one({"name": name})
        if user_key is None:
            post = {
                "name": name,
                "password": password
            }
            self.accounts.insert_one(post)
        else:
            print(f"{name} already exists in database.")
    
    def update_account(self, _query, _set):
        self.accounts.find_one_and_update(_query, {"$set": _set})
    
    def fetch_account(self, name):
        return self.accounts.find_one({"name": name})

    def add_message(self, sender, to, message):
        post = {
            "from": sender,
            "to": to,
            "message": message,
            "timestamp": time.time()
        }
        self.messages.insert_one(post)
    
    def add_feed(self, sender, message):
        post = {
            "from": sender,
            "message": message,
            "timestamp": time.time()
        }
        self.feed.insert_one(post)


# Wrapper function
async def initialize():
    mongoDB = Database()


if __name__ == "__main__":
    initialize()