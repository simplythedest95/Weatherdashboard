"""Appens sidor"""

from flask import Blueprint, render_template, request

from application.stader import STADER, hitta_stad
from application.tolkning import tolka_dagar, tolka_nuvarande
from application.vader_api import VaderTjanstError, hamta_prognos

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Startsidan med stadsvalet"""
    return render_template("index.html", stader=STADER)


@main.route("/prognos")
def prognos():
    """Visar nuvarande väder och tre dagars prognos för vald stad"""
    namn = request.args.get("stad", "").strip()
    if not namn:
        return render_template(
            "fel.html", rubrik="Ingen stad vald", text="Välj en stad i listan."
        ), 400
    stad = hitta_stad(namn)
    if stad is None:
        return render_template(
            "fel.html", rubrik="Staden finns inte", text=f"{namn} finns inte i listan."
        ), 404
    try:
        data = hamta_prognos(stad["lat"], stad["lon"])
        nu = tolka_nuvarande(data)
        dagar = tolka_dagar(data)
    except VaderTjanstError as fel:
        return render_template(
            "fel.html", rubrik="Vädertjänsten svarar inte", text=str(fel)
        ), 502

    return render_template("prognos.html", stad=stad, nu=nu, dagar=dagar)
