import pymongo
import os


class Database(object):
    # URI = "mongodb://127.0.0.1:27017"
    URI = os.environ.get("MONGODB_URI")
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        # Database.DATABASE = client['webtools']
        Database.DATABASE = client['heroku_2xm1tkl4']
        # Can also use Database.DATABASE = client.get_default_database()

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)
        # upsert option can be used to insert a new document if a matching document does not exist

    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)
        