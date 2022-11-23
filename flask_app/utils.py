from datetime import datetime
import re

def current_time() -> str:
    return datetime.now().strftime("%B%d%Y%H%M%S")

def is_date(data):
    regex = "(^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$)|(^present$)"
    return bool(re.match(regex, data))

def is_url(url):
    regex = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
    return bool(re.match(regex, url))