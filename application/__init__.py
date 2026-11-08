"""Väderappen: skapar Flask-appen"""

from flask import Flask


def create_app(config=None):
    """Skapar och konfigurerar en ny app"""
    app = Flask(__name__)
    if config:
        app.config.update(config)
    from application.routes import main

    app.register_blueprint(main)
    return app
