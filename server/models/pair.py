import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import numpy as np
import json
from app import db
from app import database


class CompareUsers():

    def append_user_match(self, user1, user2):
        username1 = user1["username"]
        username2 = user2["username"]
        user1_survey = db.users.find_one({"username": username1}).get("survey")[0]
        user2_survey = db.users.find_one({"username": username2}).get("survey")[0] 

        #print(f'user_1: {user1_survey}, user_2: {user2_survey}')

        corr = (np.corrcoef(user1_survey, user2_survey) + 1)[0][1]
        if corr != 0:
            corr /= 2

        corr_str = f"{corr:.0%}"

        database.add_user_match(user1, [username2, corr_str]) 
        database.add_user_match(user2, [username1, corr_str])
        
    def compute_user_matches(self, user):
        users = db.users.find()
        for user_i in users:
            self.append_user_match(user, user_i)
