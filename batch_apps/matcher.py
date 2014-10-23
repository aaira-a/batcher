import datetime
import re


def match_partial_prefix(regex, text):
    return bool(re.search(regex, text))


def match_full_subject(regex, text):
    return bool(re.search(regex, text))


def match_and_capture_date(text, supplied_date_pattern="dd/mm/yyyy"):
    regex_noslash = '(\d{4}/\d{4})'
    regex_slash = '(\d{2}/\d{2}/\d{4})'

    supplied_date_pattern = re.sub('[()]', '', supplied_date_pattern)

    if supplied_date_pattern == "dd/mm/yyyy":
        regex = regex_slash
        extraction_format = "%d/%m/%Y"

    elif supplied_date_pattern == "mm/dd/yyyy":
        regex = regex_slash
        extraction_format = "%m/%d/%Y"

    elif supplied_date_pattern == "ddmm/yyyy":
        regex = regex_noslash
        extraction_format = "%d%m/%Y"

    elif supplied_date_pattern == "mmdd/yyyy":
        regex = regex_noslash
        extraction_format = "%m%d/%Y"

    else:
        regex = regex_slash

    m = re.search(regex, text)

    if bool(m) is True:
        extracted_date = datetime.datetime.strptime(m.group(1), extraction_format)
        return extracted_date.strftime("%Y-%m-%d")

    return None


def app_match_full_subject(app, pattern):
    return bool(re.search(str(pattern), str(app)))
