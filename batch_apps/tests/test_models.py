from django.test import TestCase
from django_mailbox.models import Message
from batch_apps.matcher import *


class MessageModelTest(TestCase):

    fixtures = ['test_messages.json']

    def test_retrieve_emails_subjects_from_db(self):
        emails = Message.objects.all().order_by('id')
        expected_subjects = [
            "GPS Listings and Co-broke Opportunities Report (20/10/2014)",
            "iProperty.com Singapore Email Alert V2 - Daily Report 2010/2014",
            "Batch App - SGDailyAppTask SendExpiringNotice Success",
            "Batch App - Listing Archive 2010/2014",
            "Batch App - SGEChannel doDevelopmentXML",
            "test email sent at 2014-10-23 1739 gmt +8 and 0939 at utc",
        ]
        for email in emails:
            self.assertIn(email.subject, expected_subjects)

    def test_email_sent_time_should_be_converted_to_datetime_object_in_gmt8(self):
        email = Message.objects.get(message_id="<CAFKhJv0yhRMvdqF9JGabbHDH2Esw86Q9OZ40B52-y=MPLCyYBg@mail.gmail.com>")
        expected_object = datetime.datetime.strptime("2014-10-20 10:31:25 +0800", "%Y-%m-%d %H:%M:%S %z")
        self.assertEqual(email.sent_time, expected_object)
