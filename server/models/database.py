import pymongo
from flask import Flask, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import array
from app import db
import pandas as pd
import numpy as np

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

    #when a user enters the database or updates his survey, we append all of his matches to the database


    def append_user_match(self, user, match):
        self.db.users.find_one_and_update(
            {"username": user.get("username")}, {'$push': {'matches': match}}
            )    
        
    def append_user_match(self, user1, user2):
        username1 = user1["username"]
        username2 = user2["username"]
        user1_survey = db.users.find_one({"username": username1})["survey"] 
        user2_survey = db.users.find_one({"username": username2})["survey"]  
        corr = np.corr(user1_survey, user2_survey)

        self.append_user_match(user1, (username2, corr))
        self.append_user_match(user2, (username1, corr))
        
    def append_user(self, user):
        users = db.users.find({"survey": True})

        for user_i in users:
            self.append_user_match(user1, user2)

    def edit_user_profile(self,user):
        self.db.users.find_one_and_update(
            {"username": user.get("username")} , {'name': request.form.get("name")}
            )
        