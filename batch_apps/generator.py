import datetime
import pytz


def get_current_date_in_gmt8(self):
    current_datetime = datetime.datetime.now(pytz.timezone('Asia/Kuala_Lumpur'))
    return current_datetime.date()
