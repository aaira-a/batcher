import datetime
import re


def match_partial_prefix(regex, text):
    return bool(re.search(regex, text))


def match_full_subject(regex, text):
    return bool(re.search(regex, text))


def match_and_capture_date(text):
    regex_noslash = '(\d{4}/\d{4})'
    regex_slash = '(\d{2}/\d{2}/\d{4})'

    m = re.search(regex_noslash, text)
    if bool(m) is True:
        extracted_date = datetime.datetime.strptime(m.group(1), "%d%m/%Y")
        return extracted_date.strftime("%Y-%m-%d")

    n = re.search(regex_slash, text)
    if bool(n) is True:
        extracted_date = datetime.datetime.strptime(n.group(1), "%d/%m/%Y")
        return extracted_date.strftime("%Y-%m-%d")

    return None


def app_match_full_subject(app, pattern):
    return bool(re.search(str(pattern), str(app)))
