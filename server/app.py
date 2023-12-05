"""Module providing routing."""
from flask import Flask, render_template
import pymongo


app = Flask(
    __name__, template_folder="../client/templates", static_folder="../client/static"
)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
