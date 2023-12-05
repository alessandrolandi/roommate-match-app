"""Module providing routing."""
from flask import Flask, render_template
import pymongo


app = Flask(
    __name__, template_folder="../client/templates", static_folder="../client/static"
)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug=True)
