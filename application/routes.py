"""Appens sidor"""

from flask import Blueprint, render_template

from application.stader import STADER

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Startsidan med stadsvalet"""
    return render_template("index.html", stader=STADER)
