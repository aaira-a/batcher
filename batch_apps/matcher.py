import re


def match_partial_prefix(regex, text):
    return bool(re.search(regex, text))


def match_full_subject(regex, text):
    return bool(re.search(regex, text))


def match_and_capture_date(regex, text):
    m = re.search(regex, text)
    return m.group(1)


def app_match_full_subject(app, pattern):
    return bool(re.search(str(pattern), str(app)))
