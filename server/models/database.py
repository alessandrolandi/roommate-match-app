import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


class Database():
    def get_connection(self):
        
        from app import uri
        
        # Connect to MongoAtlas
        mongo = MongoClient(uri, server_api=ServerApi("1"))

        try:
            mongo.admin.command("ping")
            print("Successfully connected to MongoDB!")
        except Exception as e:
            print(e)
        
        return mongo.db
