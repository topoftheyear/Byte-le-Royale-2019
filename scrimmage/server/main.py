import os
import datetime
from flask import Flask, request, redirect, url_for, g, Response, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from functools import wraps
from bson import json_util
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest
from uuid import uuid4
from validate_script import validate

ADMIN_team_name = "BL_ROYALE_ADMIN"
ADMIN_PASSWORD = "bl_royale_admin_123"

UPLOAD_FOLDER = os.path.abspath('uploads')

SIZE_LIMIT = 5

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app)
mongo = PyMongo(app)



class SubmissionState:
    waiting = "Waiting for next scrimmage match."
    running = "Submission running."
    error = "Client terminated with an error."
    finished = "Submission finished running."


# Auth
def check_auth(team_name, password):
    """This function is called to check if a team_name /
    password combination is valid.
    """
    if team_name == ADMIN_team_name:
        return password == ADMIN_PASSWORD
    else:
        user = mongo.db.users.find_one({"team_name": team_name})

        if user:
            return check_password_hash(user["password_hash"], password)
    return False


def check_admin(team_name, password):
    return team_name == ADMIN_team_name and password == ADMIN_PASSWORD


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        print(auth)
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def requires_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


# API Routes
@app.route("/announcements", methods=["GET"])
def get_announcements():
    announcements = [a for a in mongo.db.announcements.find()]

    return Response(
        json_util.dumps({"announcements": announcements}),
        mimetype="application/json"
    )


@app.route("/announcements", methods=["POST"])
@requires_admin
def add_announcement():
    data = request.json

    if "message" not in data:
        raise BadRequest("Key 'message' not present in payload.")

    if "title" not in data:
        raise BadRequest("Key 'title' not present in payload.")

    mongo.db.announcements.insert_one({
        "title": data["title"],
        "message": data["message"],
        "posted_date": str(datetime.datetime.now())
    })
    return "success"


@app.route("/announcements", methods=["DELETE"])
@requires_admin
def clear_announcements():
    all = request.args.get("all", False)

    if all:
        mongo.db.announcements.delete_many({})

    else:
        # Delete only one
        # TODO update to allow deleting one
        pass

    return "Success"



@app.route("/register", methods=["POST"])
def register_team():
    data = request.json

    if not mongo.db.config.find_one({"registration_open": True}):
        raise BadRequest("Registration is closed.")

    if "team_name" not in data:
        raise BadRequest("Team name is required.")

    team_name = data["team_name"]
    password = str(uuid4())

    if len("".join(team_name.split())) == 0:
        raise BadRequest("Team name cannot be empty or white space.")

    team_name = team_name.strip()

    if mongo.db.users.find_one({"team_name": team_name}):
        raise BadRequest(f"Team with name '{team_name}' already exists.")

    mongo.db.users.insert_one({
        "team_name": team_name,
        "password_hash": generate_password_hash(password),
        "submissions": []
    })

    return jsonify({"auth_token": password})

@app.route("/registration/open", methods=["POST"])
@requires_admin
def registration_open():
    mongo.db.config.insert_one({"registration_open": True})
    return "success"

@app.route("/registration/close", methods=["POST"])
@requires_admin
def registration_close():
    mongo.db.config.delete_many({"registration_open": True})
    return "success"


@app.route("/submissions", methods=["POST"])
@requires_auth
def upload_file():

    if request.content_length > SIZE_LIMIT*1024*1024:
        raise BadRequest("Uploaded client too large. sent: {}MB max: {}MB".format(request.content_length/1024/1024, SIZE_LIMIT))

    data = request.json
    user = get_user()

    team_name = user["team_name"]
    filename = "".join(x for x in team_name if x.isalnum()) + ".py"
    file_data = data["file_data"]

    # add submission to db
    submissions = user["submissions"]
    no_subs = len(submissions)
    time = datetime.datetime.now()
    submissions.append({
        "submission_no": no_subs,
        "name": f"Submission #{no_subs} ({time})",
        "file_name": filename,
        "upload_date": time,
        "submission_state": SubmissionState.waiting,
        "stats": {}
    })

    mongo.db.users.update_one({"team_name": team_name}, {"$set": {
        "submissions": submissions
    }})


    # save file to disk
    with open(os.path.join(UPLOAD_FOLDER, filename), "w") as f:
        f.write(file_data)

    return jsonify({"submission_no": no_subs})


@app.route("/submissions", methods=["GET"])
@requires_admin
def get_submissions():
    team_data = []
    for team in mongo.db.users.find():
        most_recent_submission = next(sorted(team["submissions"], key=lambda e:e["submission_no"], reverse=True))

        with open(os.path.join(UPLOAD_FOLDER, team["file_name"]), "r") as f:
            client_data = f.read()

        team_data.append({
            "team_name": team["team_name"],
            "client_data": client_data,
            "submission_info": most_recent_submission["submission_no"],
        })

    return Response(
        json_util.dumps({"teams_": team_data}),
        mimetype="application/json"
    )



@app.route("/report", methods=["POST"])
@requires_admin
def upload_game_info():
    """Used by the runner to upload the client logs, results, update leaderboards"""
    json = request.json




# ######### Helpers

def get_user():
    auth = request.authorization
    if not auth:
        return None

    user = mongo.db.users.find_one({"team_name": auth.username})

    return user


if __name__ == "__main__":
    app.run()
