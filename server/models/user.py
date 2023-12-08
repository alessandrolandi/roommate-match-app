from flask import Flask, request
from passlib.hash import pbkdf2_sha256
import uuid


class User:
    def create(self):
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get("name"),
            "password": request.form.get("password"),
            "matches": [],
        }

        user["password"] = pbkdf2_sha256.encrypt(user["password"])
        
        return user

