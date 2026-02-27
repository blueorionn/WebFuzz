"""Core views."""

import os
from flask import current_app, render_template, send_file
from flask.views import MethodView


class IndexView(MethodView):
    def get(self):
        return render_template("index.html")


def serve_favicon_handler():
    path = os.path.join(current_app.config["APP_DIR"], f"static/public/favicon.ico")

    return send_file(path, mimetype="image/x-icon")
