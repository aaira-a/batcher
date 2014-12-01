import datetime
import re


def match_subject(regex, text):
    regex = str(regex).replace("(", "\\(").replace(")", "\\)")
    return bool(re.search(str(regex), str(text)))


def capture_date(text, supplied_date_pattern="dd/mm/yyyy"):
    regex_noslash = '(\d{4}/\d{4})'
    regex_slash = '(\d{1,2}/\d{1,2}/\d{4})'

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
        return

    m = re.search(regex, text)

    if bool(m) is True:
        extracted_date = datetime.datetime.strptime(m.group(1), extraction_format)
        return extracted_date.strftime("%Y-%m-%d")


def app_match_full_subject(app, pattern):
    return bool(re.search(str(pattern), str(app)))


def match_email_subject_to_app(subject, app):
    pattern_list = app.pattern_set.filter(is_active=True)

    if len(pattern_list) == 1:
        return match_subject(pattern_list[0], subject)

    if len(pattern_list) >= 2:
        results = []
        for pattern in pattern_list:
            results.append(match_subject(pattern, subject))
        return all(results)
