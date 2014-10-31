from django.test import TestCase
from django_mailbox.models import Message
from batch_apps.models import App, Day, Execution
from batch_apps.matcher import *
from datetime import date


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


class DayModelTest(TestCase):

    def test_day_model_should_return_yyyy_mm_dd_as_string_representation(self):
        day = Day.objects.create(date=datetime.date(2014, 10, 20))
        self.assertEqual(day.__str__(), "2014-10-20")


class ExecutionModelTest(TestCase):

    def test_execution_model_should_return_string_for_successful_execution(self):
        app_ = App.objects.create(name="My App 001")
        day_ = Day.objects.create(date=datetime.date(2014, 10, 20))
        execution = Execution.objects.create(day=day_, app=app_, is_executed=True)
        self.assertEqual(execution.__str__(), "My App 001 executed on 2014-10-20")

    def test_execution_model_should_return_string_for_pending_execution(self):
        app_ = App.objects.create(name="My App 001")
        day_ = Day.objects.create(date=datetime.date(2014, 10, 20))
        execution = Execution.objects.create(day=day_, app=app_, is_executed=False, is_due_today=True)
        self.assertEqual(execution.__str__(), "My App 001 yet to be executed on 2014-10-20")

    def test_execution_model_should_return_string_for_inactive_execution(self):
        app_ = App.objects.create(name="My App 001")
        day_ = Day.objects.create(date=datetime.date(2014, 10, 20))
        execution = Execution.objects.create(day=day_, app=app_, is_executed=False, is_due_today=False)
        self.assertEqual(execution.__str__(), "My App 001 not to be executed on 2014-10-20")
