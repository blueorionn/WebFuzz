"""API views."""

import os
import json
import pandas as pd

from pathlib import Path
from flask import request, current_app, jsonify
from flask.views import MethodView
from webfuzz.utils import is_valid_url

from .misc import FuzzRequestDataType, validate_status_codes, validate_cookies
from .func import check_is_ffuf_installed, fuzz_request_with_ffuf


class IndexView(MethodView):
    def get(self):
        return jsonify({"message": "welcome to api!"}), 200


class FuzzView(MethodView):
    def post(self):
        data: FuzzRequestDataType = request.get_json()

        # data validation
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        # converting data to dict
        try:
            data = json.loads(data)
        except Exception as e:
            return jsonify({"error": "Failed to convert data to dict"}), 500

        # data parameters validation
        if not data.get("FUZZ_URL"):
            return jsonify({"error": "FUZZ_URL is required"}), 400
        if not is_valid_url(data["FUZZ_URL"]):
            return jsonify({"error": "Invalid URL"}), 400

        if not data.get("FUZZ_METHOD"):
            return jsonify({"error": "FUZZ_METHOD is required"}), 400
        if data.get("FUZZ_METHOD") not in ["GET", "POST", "PUT", "DELETE"]:
            return jsonify({"error": "Invalid FUZZ_METHOD"}), 400

        if not isinstance(data["FUZZ_DELAY"], int):
            return jsonify({"error": "Invalid FUZZ_DELAY"}), 400

        if data["FUZZ_FILTER_STATUS_CODES"] and not validate_status_codes(
            data["FUZZ_FILTER_STATUS_CODES"]
        ):
            return jsonify({"error": "Invalid FUZZ_FILTER_STATUS_CODES"}), 400

        if data["FUZZ_MATCH_STATUS_CODES"] and not validate_status_codes(
            data["FUZZ_MATCH_STATUS_CODES"]
        ):
            return jsonify({"error": "Invalid FUZZ_MATCH_STATUS_CODES"}), 400

        if not data.get("FUZZ_PAYLOAD"):
            return jsonify({"error": "FUZZ_PAYLOAD is required"}), 400
        if len(data.get("FUZZ_PAYLOAD")) == 0:
            return jsonify({"error": "FUZZ_PAYLOAD cannot be empty"}), 400

        if data.get("FUZZ_METHOD") in ["POST", "PUT"] and (
            not data.get("FUZZ_POST_DATA") or len(data.get("FUZZ_POST_DATA")) == 0
        ):
            return (
                jsonify(
                    {"error": "FUZZ_POST_DATA is required for POST and PUT methods"}
                ),
                400,
            )

        if data.get("FUZZ_COOKIES") and not validate_cookies(data["FUZZ_COOKIES"]):
            return jsonify({"error": "Invalid FUZZ_COOKIES"}), 400

        # check if ffuf is installed
        if not check_is_ffuf_installed():
            return jsonify({"error": "ffuf is not installed in the server"}), 500

        fuzz_result = fuzz_request_with_ffuf(**data)
        return jsonify(fuzz_result), fuzz_result.get("status", 500)


class OutputView(MethodView):
    def get(self):
        filename = request.args.get("filename", None)
        if filename:
            if Path(
                os.path.join(current_app.config["FFUF_OUTPUT_PATH"], filename)
            ).is_file():
                df = pd.read_csv(
                    os.path.join(current_app.config["FFUF_OUTPUT_PATH"], filename)
                )
                data = df.to_dict(orient="records")
                return jsonify({"result": {"data": data}}), 200
            else:
                return jsonify({"result": {"error": "CSV file not found."}}), 404
        else:
            return (
                jsonify({"result": {"error": "Filename parameter is required."}}),
                400,
            )
