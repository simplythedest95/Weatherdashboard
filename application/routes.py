"""Appens sidor"""

from flask import Blueprint, render_template, request

from application.stader import STADER, hitta_stad
from application.tolkning import tolka_dagar, tolka_nuvarande
from application.vader_api import hamta_prognos

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Startsidan med stadsvalet"""
    return render_template("index.html", stader=STADER)


@main.route("/prognos")
def prognos():
    """Visar nuvarande väder och tre dagars prognos för vald stad"""
    stad = hitta_stad(request.args.get("stad"))
    data = hamta_prognos(stad["lat"], stad["lon"])
    return render_template(
        "prognos.html",
        stad=stad,
        nu=tolka_nuvarande(data),
        dagar=tolka_dagar(data),
    )
