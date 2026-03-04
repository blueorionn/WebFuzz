"""API URLs"""

from flask import Blueprint
from .views import IndexView, FuzzView

# Create a blueprint for the API module
blueprint = Blueprint("api", __name__, url_prefix="/api")

# Define the URL rules for the API module
index_view = IndexView.as_view("base")
blueprint.add_url_rule("/", view_func=index_view)

fuzz_view = FuzzView.as_view("fuzz")
blueprint.add_url_rule("/fuzz", view_func=fuzz_view)
