from flask import Flask, jsonify, request, session
from passlib.hash import pbkdf2_sha256
from app import db
from models.user import User


class UserAuthentication:
    def sign_up(self):
        user = UserFactory().get_user()

        if db.users.find_one({"name": user["name"]}):
            return jsonify({"error": "Name already in use"}), 400

        if db.users.insert_one(user):
            return self.start_session(user)

        return jsonify({"error": "Something went wrong"}), 400


    def login(self):
        user = db.users.find_one({"name": request.form.get("name")})

        if user and pbkdf2_sha256.verify(
            request.form.get("password"), user["password"]
        ):
            return self.start_session(user)

        return jsonify({"error": "Invalid login credentials "}), 401


    def start_session(self, user):
        del user["password"]
        session["logged_in"] = True
        session["user"] = user

        return jsonify(user), 200


    def sign_out(self):
        session.clear()
