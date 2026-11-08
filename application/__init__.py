"""Väderappen: skapar Flask-appen"""

from flask import Flask


def create_app(config=None):
     """Skapar och konfigurerar en ny app"""
     app = Flask(__name__)
     if config:
          app.config.update(config)
     from application.routes import main

     app.register_blueprint(main)
     from application.felsidor import sida_saknas

     app.register_error_handler(404, sida_saknas)
     from application.filter import nederbord, temperatur, veckodag, vind
     for funktion in (temperatur, vind, nederbord, veckodag):
          app.add_template_filter(funktion)     
     return app
