from django.db import connection
from django_mailbox.models import Message

import os
import sqlite3


def get_sqlite_filesize(path='db.sqlite3'):
    try:
        filesize_unformatted = os.path.getsize(path)
        filesize_humanised = sizeof_formatter(filesize_unformatted)
        return filesize_humanised
    except:
        return 'N/A'


def sizeof_formatter(num, suffix='B'):
    '''
    http://stackoverflow.com/a/1094933/3480790
    '''
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0


def strip_message_body():
    all_messages = Message.objects.all()
    all_messages.update(body='')


def vacuum_sqlite(path=None):
    if path:
        my_connection = sqlite3.connect(path)
        cursor = my_connection.cursor()
    else:
        cursor = connection.cursor()

    cursor.execute("VACUUM")
