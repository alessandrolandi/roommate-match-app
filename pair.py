import pymongo
import mongo
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import numpy as np
import json

users = mongo.db.users.find()
survey = dict()
for user in users:
    #user.survey should be stored as a dictionary, with keys uniform across all users
    # corresp. to questions and values corresponding to numerical values for survey questions
    survey[f'{user.name}'] = survey.append(user.survey)

survey_df = pd.DataFrame(survey)
corr = survey_df.corr()

for user in users:
    edit_matches(user)
    user.matches = corr.loc[user].sort_values()
    user.save()

def edit_user(user_id):
    name = request.form.get("fname")
    number = request.form.get("pnumber")
    email = request.form.get("email")

    doc = {
        "matches": 
        "fullName": name,
        "phoneNumber": number,
        "emailAddress": email,
        "favorite": False,
    }

    mongo.db.contacts.update_one(
        {"_id": ObjectId(contact_id)}, 
        { "$set": doc }
    )

    return redirect(url_for('display_all_contacts'))