import re
from datetime import datetime


def current_time() -> str:
    return datetime.now().strftime("%B%d%Y%H%M%S")


def is_date(data):
    regex = "(^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$)|(^present$)"
    return bool(re.match(regex, data))


def is_url(url):
    regex = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
    return bool(re.match(regex, url))


def translate(property):
    dictionary = {
        "HomepageDetails": "Homepage Details",
        "Experience": "Experience",
        "Project": "Project",
        "company_name": "Company Name",
        "start_date": "Start Date",
        "end_date": "End Date",
        "full_name": "Full Name",
        "project_name": "Project Name",
        "position": "Position",
        "bullet": "Bullet",
        "technology": "Technology",
        "long_description": "Long Description",
    }

    if property in dictionary:
        return dictionary[property]
    else:
        return property
