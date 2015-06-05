from django.test import TestCase

from batch_apps.maintenance import (
    get_sqlite_filesize,
    strip_message_body,
    vacuum_sqlite
    )

from django_mailbox.models import Message

import os
import shutil


class SQLiteFileSizeTest(TestCase):

    def test_sqlite_filesize_should_be_human_readable(self):
        filesize = get_sqlite_filesize('batch_apps/fixtures/test_db.sqlite3')
        self.assertEqual(filesize, '160.0 KiB')

    def test_sqlite_filesize_should_be_na_if_not_readable(self):
        filesize = get_sqlite_filesize('not_sqlite.sqlite')
        self.assertEqual(filesize, 'N/A')


class MessageBodyStripTest(TestCase):

    fixtures = ['test_messages.json']

    def test_strip_body_replaces_body_with_empty_string(self):
        emails = Message.objects.all()
        for email in emails:
            self.assertTrue(email.body)

        strip_message_body()

        emails_recheck = Message.objects.all()
        for email in emails_recheck:
            self.assertFalse(email.body)


class SQLiteVacuumTest(TestCase):

    def setUp(self):
        self.original = 'batch_apps/fixtures/test_db.sqlite3'
        self.temp = 'batch_apps/fixtures/test_db_temp.sqlite3'
        shutil.copy(self.original, self.temp)

    def tearDown(self):
        os.remove(self.temp)

    def test_vacuum_sqlite_should_reduce_filesize(self):
        before_filesize = os.path.getsize(self.temp)

        vacuum_sqlite('batch_apps/fixtures/test_db_temp.sqlite3')
        after_filesize = os.path.getsize(self.temp)

        self.assertTrue(after_filesize < before_filesize)
