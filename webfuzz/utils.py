"""Utility functions."""

import re
import secrets
import uuid


def generate_secret_key():
    """Generate a random string of 50 characters."""
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    secret_len = 50
    return "".join(secrets.choice(chars) for i in range(secret_len))


def is_valid_uuid_v4(id_str):
    try:
        uuid_obj = uuid.UUID(id_str, version=4)
        return str(uuid_obj) == id_str
    except ValueError:
        return False


def hyphenate_text(text: str):
    return "-".join(text.lower().split(" "))


def is_valid_url(url: str) -> bool:
    # Basic URL validation
    regex = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"  # ...or ipv4
        r"\[?[A-F0-9]*:[A-F0-9:]+\]?)"  # ...or ipv6
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return re.match(regex, url) is not None
