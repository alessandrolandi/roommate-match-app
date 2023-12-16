import pymongo
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import numpy as np
import json
from app import db

users = list(db.user.find({"survey": True}))
print(users)

survey = dict()
for user in users:
    #user.survey should be stored as a dictionary, with keys uniform across all users
    # corresp. to questions and values corresponding to numerical values for survey questions
    #insert 
    survey.append(user["survey"])


survey_df = pd.DataFrame(survey)
corr = survey_df.corr()

