"""Core URLs"""

from flask import Blueprint
from .views import IndexView, serve_favicon_handler

# Create a blueprint for the core module
blueprint = Blueprint("core", __name__)

# Define the URL rules for the core module
index_view = IndexView.as_view("home")
blueprint.add_url_rule("/", view_func=index_view)


@blueprint.route("/favicon.ico")
def favicon():
    return serve_favicon_handler()
