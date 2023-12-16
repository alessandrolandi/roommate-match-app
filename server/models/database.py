import pymongo
from flask import Flask, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import array
import numpy as np

class DatabaseProxy:
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

    def add_user_match(self, user, match):
        self.db.users.find_one_and_update(
            {"username": user.get("username")}, {'$push': {'matches': match}}
            )   
    
    def edit_user_profile(self,user):
        self.db.users.find_one_and_update(
            {"username": user.get("username")},
            {"$set": {"name": request.form.get("name")}},
        )

    def add_message(self, user, message):
        self.db.messages.insert_one(
            {"message": message, "user": user, "time": datetime.today()}
        )

    def get_messages(self):
        messages = self.db.messages.find()
        return messages
