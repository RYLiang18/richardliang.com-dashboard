from datetime import datetime
import re

def current_time() -> str:
    return datetime.now().strftime("%B%d%Y%H%M%S")

def is_date(data):
    regex = r"(^[\d]{2}/[\d]{2}/[\d]{4}$)|(^present$)"
    return bool(re.search(regex, data))

url_regex = r"^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"