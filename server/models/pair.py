import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import numpy as np
import json
from app import db


class CompareUsers():

    def append_user_match(self, user1, user2):
        username1 = user1["username"]
        username2 = user2["username"]
        user1_survey = db.users.find_one({"username": username1})["survey"] 
        user2_survey = db.users.find_one({"username": username2})["survey"]  
        corr = np.corr(user1_survey, user2_survey)

        db.add_user_match(user1, (username2, corr))
        db.add_user_match(user2, (username1, corr))
        
    def compute_user_matches(self, user):
        users = db.users.find({"survey": True})

        for user_i in users:
            self.append_user_match(user, user_i)

