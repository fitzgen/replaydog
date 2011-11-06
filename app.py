from flask import (Flask, abort, flash, g, redirect, render_template, request,
                   send_from_directory, url_for)
import data
import settings

app = Flask(__name__)


# Before/After request hooks

@app.before_request
def before_request():
    """
    Open a connection to the database at the start of each request.
    """
    g.conn = data.connect()

@app.teardown_request
def teardown_request(exception):
    """
    Close the connection to the database at the end of each request.
    """
    if hasattr(g, "conn"):
        g.conn.close()


# Routes

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Index page displays the upload form on GET, and saves replays on POST.
    """
    if request.method == "POST":
        replay_file = request.files["replay"]
        replay_id = data.save_replay(g.conn, replay_file)
        if replay_id:
            return redirect(url_for("replay_detail", replay_id=replay_id))
        else:
            flash("Sorry, that file doesn't appear to be a valid StarCraft II replay.")
            render_template("index.html")
    else:
        return render_template("index.html")

@app.route("/<replay_id>", methods=["GET"])
def replay_detail(replay_id):
    """
    Display the details of a replay.
    """
    details = data.get_replay_details(g.conn, replay_id)
    if details:
        return render_template("replay_detail.html", **details)
    else:
        abort(404)

@app.route("/r/<replay_id>", methods=["GET"])
def replay_file(replay_id):
    """
    Send the actual replay file to the client.
    """
    replay_file = data.file_for_replay(g.conn, replay_id)
    if replay_file:
        return send_from_directory(settings.UPLOAD_DIRECTORY, replay_file)
    else:
        abort(404)


# Error handlers

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(error):
    return render_template("500.html"), 500

# Dev server

if __name__ == '__main__':
    app.run(debug=True)
