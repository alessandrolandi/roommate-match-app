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
from models.database import DatabaseProxy
from flask_socketio import SocketIO, join_room, leave_room, send
import eventlet



# Create connection to database
load_dotenv()
uri = os.getenv("URI")
database = DatabaseProxy()
db = database.db


# Create app instance
app = Flask(
    __name__, template_folder="../client/templates", static_folder="../client/static"
)
app.secret_key = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

fauxData = {}


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


@app.route("/register/survey", methods=["GET", "POST"])
@login_required
def survey():
    if request.method == "POST":
        from models.authentication import UserAuthentication

        return UserAuthentication().survey(session["user"])
    return render_template("survey.html")


@app.route("/signout")
def signout():
    from models.authentication import UserAuthentication

    UserAuthentication().sign_out()

    return redirect(url_for("login"))


@app.route("/home/")
@login_required
def home():
    matches = session["user"].get("matches")
    sorted_matches = sorted(matches, key = lambda x: int(x[1][:-1]), reverse = True)
    return render_template("home.html", matches=sorted_matches)


@app.route("/profile/", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        from models.authentication import UserAuthentication

        database.edit_user_profile(session["user"])
        return  UserAuthentication().edit_session_name()

    return render_template("profile.html", user=session["user"])


@app.route("/chat")
@login_required
def chat():
    messages = database.get_messages()
    return render_template(
        "chat.html", messages=messages, username=session["user"]["name"], room=1
    )


@socketio.on("send_message")
def handle_send_message_event(data):
    app.logger.info(
        "{} has sent message to the room {}: {}".format(
            data["username"], data["room"], data["message"]
        )
    )
    database.add_message(session["user"].get("name"), data["message"])
    socketio.emit("receive_message", data, room=data["room"])


@socketio.on("join_room")
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data["username"], data["room"]))
    join_room(data["room"])
    socketio.emit("join_room_announcement", data)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=3000, debug=True)
