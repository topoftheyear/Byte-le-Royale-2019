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
import json

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
        "runs": []
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
        most_recent_submission = next(iter(sorted(team["submissions"], key=lambda e:e["submission_no"], reverse=True)), None)
        if most_recent_submission is None:
            continue

        with open(os.path.join(UPLOAD_FOLDER, most_recent_submission["file_name"]), "r") as f:
            client_data = f.read()

        team_data.append({
            "team_name": team["team_name"],
            "client_data": client_data,
            "submission_no": most_recent_submission["submission_no"],
        })

        subs = team["submissions"]
        idx = subs.index(most_recent_submission)
        subs[idx]["submission_state"] = SubmissionState.running

        # mark team submission as running
        mongo.db.users.update_one({"team_name": team["team_name"]}, {"$set": {
            "submissions": subs
        }})


    return Response(
        json_util.dumps({"teams": team_data}),
        mimetype="application/json"
    )

@app.route("/report/run", methods=["POST"])
@requires_admin
def update_run_no():
    data = request.json


    run_no = get_latest_run_no()

    if run_no == None:
        run_no = 1
    else:
        run_no += 1


    mongo.db.runs.insert_one({
        "run_no": run_no
    })

    return "ok"


@app.route("/report/ranking", methods=["POST"])
@requires_admin
def upload_game_ranking():
    data = request.json
    run_no = get_latest_run_no()
    mongo.db.leaderboard.insert_one({
        "run_number": run_no,
        "leaderboard": data
    })

    return "ok"


@app.route("/report/game_logs", methods=["POST"])
@requires_admin
def upload_game_logs():
    data = request.json
    run_no = get_latest_run_no()

    if not os.path.exists("runs"):
        os.makedirs("runs")

    old_result_file = "runs/{}_result.json".format(run_no-1)
    old_log_files = "runs/{}.tar".format(run_no-1)

    if os.path.exists(old_result_file):
        os.unlink(old_result_file)

    if os.path.exists(old_log_files):
        os.unlink(old_log_files)

    # insert into db
    result_file = "runs/{}_result.json".format(run_no)
    game_data_file = "runs/{}_game_data.json".format(run_no)
    log_files = "runs/{}.tar".format(run_no)
    with open(log_files, "w") as f:
        f.write(data["game_log"])

    with open(result_file, "w") as f:
        json.dump(data["results"], f)

    with open(game_data_file, "w") as f:
        json.dump(data["game_data"], f)

    return "ok"

@app.route('/report/game_logs', methods=["GET"])
@app.route("/report/game_logs/<int:run>", methods=["GET"])
@requires_admin
def get_game_logs(run=None):

    if run is None:
        run = get_latest_run_no()

    if run is None:
        return Response('No runs availaible', status=204)

    result_file = "runs/{}_result.json".format(run)
    log_files = "runs/{}.tar".format(run)
    game_data_file = "runs/{}_game_data.json".format(run)
    with open(log_files, "rb") as f:
        log_data = f.read()

    with open(result_file, "r") as f:
        results_data = f.read()

    with open(game_data_file, "r") as f:
        game_data = f.read()
        
    results_data = json.loads(results_data)
    results_data["run_no"] = run
    results_data = json.dumps(results_data)

    return jsonify({
        "results": results_data,
        "game_data": game_data,
        "log_data": log_data.decode("utf-8")
    })

@app.route("/report/client_log", methods=["POST"])
@requires_admin
def upload_client_logs():
    data = request.json

    user = get_user(data["team_name"])
    run_no = get_latest_run_no()

    submissions = user["submissions"]
    most_recent_submission = sorted(
                    submissions,
                    key=lambda e:e["submission_no"], reverse=True)[0]

    index = submissions.index(most_recent_submission)

    submissions[index]["submission_state"] = SubmissionState.finished

    # get submissions older than the last 5
    cutoff = run_no-5
    to_save = list(filter(
            lambda s: s["run_number"]>cutoff,
            submissions[index]["runs"]))

    print(len(to_save))

    submissions[index]["runs"] = None
    submissions[index]["runs"] = to_save
    submissions[index]["runs"].append({
        "run_number": run_no,
        "log": data["log"]
    })

    mongo.db.users.update_one({"team_name": user["team_name"]}, {"$set": {
        "submissions": submissions
    }})

    return "ok"

@app.route("/submissions/list", methods=["GET"])
@requires_auth
def get_client_submissions():
    user = get_user()
    s = []
    for sub in user["submissions"]:
        s.append({
            "submission_no": sub["submission_no"],
            "name": sub["name"],
            "file_name": sub["file_name"],
            "upload_date": sub["upload_date"],
            "submission_state": sub["submission_state"]
        })

    return Response(
        json_util.dumps(s),
        mimetype="application/json"
    )

@app.route("/report/submissions/<int:submission_no>", methods=["GET"])
@requires_auth
def get_client_logs(submission_no):

    user = get_user()

    submission = next(
            iter(filter(
                lambda s: s["submission_no"] == submission_no,
                user["submissions"])), None)

    return jsonify(submission)

@app.route("/leaderboard", methods=["GET"])
def get_leaderboard():

    leaderboard = next(iter(
        mongo.db.leaderboard.find({}, sort=[("run_number", -1)])),
        None)

    return Response(
        json_util.dumps(leaderboard),
        mimetype="application/json"
    )

@app.route("/leaderboard/<int:run_no>", methods=["GET"])
def get_leaderboard_by_no(run_no):

    leaderboard = next(iter(
        mongo.db.leaderboard.find({"run_number": run_no})),
        None)

    return Response(
        json_util.dumps(leaderboard),
        mimetype="application/json"
    )



# ######### Helpers

def get_user(team_name=None):
    if team_name is None:
        auth = request.authorization
        if not auth:
            return None

        user = mongo.db.users.find_one({"team_name": auth.username})

        return user
    else:
        user = mongo.db.users.find_one({"team_name": team_name})
        return user

def get_latest_run_no():
    run_info = mongo.db.runs.find_one({}, sort=[("run_no", -1)])
    if run_info == None:
        return None
    else:
        return run_info["run_no"]


if __name__ == "__main__":
    app.run()
