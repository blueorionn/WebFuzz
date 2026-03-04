from typing import TypedDict, Literal


class FuzzRequestDataType(TypedDict):
    FUZZ_URL: str
    FUZZ_METHOD: Literal["GET", "POST", "PUT", "DELETE"]
    FUZZ_DELAY: int
    FUZZ_FILTER_STATUS_CODES: str
    FUZZ_MATCH_STATUS_CODES: str
    FUZZ_PAYLOAD: str
    FUZZ_POST_DATA: str
    FUZZ_USER_AGENT: str
    FUZZ_COOKIES: str


def validate_status_codes(status_codes: str) -> bool:
    if not status_codes:
        return False
    codes = status_codes.split(",")
    for code in codes:
        if not code.strip().isdigit():
            return False
    return True


def validate_cookies(cookies: str) -> bool:
    if not cookies:
        return False
    cookie_list = cookies.split(";")
    for cookie in cookie_list:
        if not cookie.strip():
            return False
    return True
