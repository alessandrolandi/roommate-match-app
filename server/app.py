"""Module providing routing."""
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    abort,
    url_for,
    make_response,
    jsonify,
    session,
)
from functools import wraps

load_dotenv()
uri = os.getenv("URI")

mongo = MongoClient(uri, server_api=ServerApi("1"))

try:
    mongo.admin.command("ping")
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Create an instance of the database
db = mongo.db

app = Flask(
    __name__, template_folder="../client/templates", static_folder="../client/static"
)

app.secret_key = os.getenv("SECRET_KEY")


# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("login"))

    return wrap


# Routes
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        from models.authentication import UserAuthentication

        return UserAuthentication().login()
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        from models.authentication import UserAuthentication

        return UserAuthentication().signup()
    return render_template("registration.html")


@app.route("/signout")
def signout():
    from models.authentication import UserAuthentication
    UserAuthentication().signout()
    
    return redirect(url_for('login'))


@app.route("/home/")
@login_required
def home():
    return render_template("home.html")


@app.route("/chat")
@login_required
def chat():
    return render_template("chat.html")


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
