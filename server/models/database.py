import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import array

class Database:
    db = ""
    
    def __init__(self):
        from app import uri

        # Connect to MongoAtlas
        mongo = MongoClient(uri, server_api=ServerApi("1"))

        try:
            mongo.admin.command("ping")
            print("Successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        self.db = mongo.db


    def get_users(self):
        users = list(self.db.users.find())

        return users


    def get_matched_users(self, user):
        session_matches = user.get("matches")
        
        matches = []
        for match in session_matches:
            matches.append(
                self.db.users.find_one({"username": match },{"password": False},{"matches": False})
            )
        
        return matches


    def add_user_matches(self, user, matches):
        self.db.users.find_one_and_update(
            {"username": user.get("username")}, {'$push': {'matches': matches}}
            )