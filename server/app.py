"""Module providing routing."""
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session,
)
import os
from dotenv import load_dotenv
from functools import wraps
from models.database import Database


# Create connection to database
load_dotenv()
uri = os.getenv("URI")
database = Database()
db = database.db


#Create app instance
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

        return UserAuthentication().sign_up()
    return render_template("registration.html")


@app.route("/signout")
def signout():
    from models.authentication import UserAuthentication

    UserAuthentication().sign_out()

    return redirect(url_for("login"))


@app.route("/home/")
@login_required
def home():
    matches = database.get_matched_users(session["user"])
    return render_template("home.html", matches=matches)


@app.route("/chat")
@login_required
def chat():
    return render_template("chat.html")


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=session["user"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
