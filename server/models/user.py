from flask import Flask, jsonify, request, session, redirect, url_for
from passlib.hash import pbkdf2_sha256
from app import mongo
import uuid


class User:
    def start_session(self, user):
        del user["password"]
        session["logged_in"] = True
        session["user"] = user

        return jsonify(user), 200

    def signup(self):
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get("name"),
            "password": request.form.get("password"),
        }

        user["password"] = pbkdf2_sha256.encrypt(user["password"])

        if mongo.db.users.find_one({"name": user["name"]}):
            return jsonify({"error": "Name already in use"}), 400

        if mongo.db.users.insert_one(user):
            return self.start_session(user)

        return jsonify({"error": "Something went wrong"}), 400

    def signout(self):
        session.clear()
        return redirect(url_for("login"))

    def login(self):
        user = mongo.db.users.find_one({"name": request.form.get("name")})

        if user and pbkdf2_sha256.verify(
            request.form.get("password"), user["password"]
        ):
            return self.start_session(user)

        return jsonify({"name": "Invalid login credentials "}), 401
