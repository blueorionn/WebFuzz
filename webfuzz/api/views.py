"""API views."""

from flask import current_app, jsonify
from flask.views import MethodView


class IndexView(MethodView):
    def get(self):
        return jsonify({"message": "welcome to api!"}), 200
