from app import app
from flask import render_template
import users
import players
import draftInit


@app.route("/")
def index():
    return render_template("index.html")