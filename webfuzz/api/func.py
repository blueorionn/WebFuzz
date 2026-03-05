import subprocess
import datetime
import uuid
import os

from flask import current_app
from .misc import validate_status_codes, validate_cookies


def check_is_ffuf_installed() -> bool:
    """Check if ffuf is installed."""
    try:
        subprocess.run(
            ["ffuf", "-h"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return True
    except subprocess.CalledProcessError:
        return False


def fuzz_request_with_ffuf(
    FUZZ_URL: str,
    FUZZ_METHOD: str,
    FUZZ_DELAY: int,
    FUZZ_FILTER_STATUS_CODES: str,
    FUZZ_MATCH_STATUS_CODES: str,
    FUZZ_PAYLOAD: str,
    FUZZ_POST_DATA: str,
    FUZZ_USER_AGENT: str,
    FUZZ_COOKIES: str,
):
    """Fuzz a request using ffuf."""

    output_file = (
        f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}_{uuid.uuid4()}.csv'
    )
    output_path = os.path.join(current_app.config["FFUF_OUTPUT_PATH"], output_file)

    cmd = [
        "ffuf",
        "-u",
        FUZZ_URL,
        "-X",
        FUZZ_METHOD,
        "-w",
        "-",  # read from stdin
        "-s",  # silent
        "-delay",
        str(FUZZ_DELAY),
        f"-o {output_path}",
        "-of csv",
    ]

    # validations
    if FUZZ_FILTER_STATUS_CODES and validate_status_codes(FUZZ_FILTER_STATUS_CODES):
        cmd.extend(["-fs", FUZZ_FILTER_STATUS_CODES])
    if FUZZ_MATCH_STATUS_CODES and validate_status_codes(FUZZ_MATCH_STATUS_CODES):
        cmd.extend(["-mc", FUZZ_MATCH_STATUS_CODES])

    # appending headers
    if FUZZ_USER_AGENT:
        cmd.extend(["-H", f"User-Agent: {FUZZ_USER_AGENT}"])
    if FUZZ_COOKIES and validate_cookies(FUZZ_COOKIES):
        cmd.extend(["-H", f"Cookie: {FUZZ_COOKIES}"])

    # appending data
    if FUZZ_METHOD in ["POST", "PUT"] and FUZZ_POST_DATA:
        cmd.extend(["-d", FUZZ_POST_DATA])

    # executing ffuf
    try:
        subprocess.run(
            cmd,
            input=FUZZ_PAYLOAD,
            stdout=subprocess.DEVNULL,  # hide normal output
            stderr=subprocess.PIPE,  # capture errors
            check=True,
        )
        return {"message": {"output_file": f"{output_path}"}, "status": 200}
    except subprocess.CalledProcessError as e:
        return {"message": {"error": e.stderr.decode().strip()}, "status": 500}
