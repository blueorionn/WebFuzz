import subprocess


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
    url: str,
    method: str,
    delay: int,
    filter_status_code: str,
    match_status_code: str,
    payload: str,
    post_data: str,
    user_agent: str,
    cookies: str,
):
    """Fuzz a request using ffuf."""

    cmd = [
        "ffuf",
        "-u",
        url,
        "-X",
        method,
        "-H",
        f"User-Agent: {user_agent}",
        "-w",
        "-",  # read from stdin
        "-delay",
        str(delay),
    ]

    process = subprocess.run(cmd, input=payload, text=True, capture_output=True)
