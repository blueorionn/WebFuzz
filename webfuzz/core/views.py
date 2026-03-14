"""Core views."""

import os
import pandas as pd
from pathlib import Path
from flask import current_app, request, render_template, send_file
from flask.views import MethodView


class IndexView(MethodView):
    def get(self):
        csv_file = request.args.get("csv", None)
        if csv_file:
            if Path(
                os.path.join(current_app.config["FFUF_OUTPUT_PATH"], csv_file)
            ).is_file():
                df = pd.read_csv(
                    os.path.join(current_app.config["FFUF_OUTPUT_PATH"], csv_file)
                )
                data = df.to_dict(orient="records")
                return render_template("index.html", context={"data": data})
            else:
                return render_template(
                    "index.html", context={"error": "CSV file not found."}
                )

        return render_template("index.html", context={})


def serve_favicon_handler():
    path = os.path.join(current_app.config["APP_DIR"], f"static/public/favicon.ico")

    return send_file(path, mimetype="image/x-icon")
