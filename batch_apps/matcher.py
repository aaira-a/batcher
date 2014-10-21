import datetime
import re


def match_partial_prefix(regex, text):
    return bool(re.search(regex, text))


def match_full_subject(regex, text):
    return bool(re.search(regex, text))


def match_and_capture_date(regex, text):
    m = re.search(regex, text)
    extracted_date = datetime.datetime.strptime(m.group(1), "%d%m/%Y")
    return extracted_date.strftime("%Y-%m-%d")


def app_match_full_subject(app, pattern):
    return bool(re.search(str(pattern), str(app)))
