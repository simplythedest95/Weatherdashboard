"""Felhanterare för appen"""

from flask import render_template


def sida_saknas(fel):
    """Visar egen sida när adressen inte finns (404)"""
    return render_template(
        "fel.html",
        rubrik="Sidan finns inte",
        text="Adressen du försökte nå finns inte i väderappen",
    ), 404
