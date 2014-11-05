from batch_apps.models import App
from django_mailbox.models import Message
from batch_apps.generator import *
from batch_apps.matcher import *


def execute_end_to_end_tasks_on_date(date_):
    day_object = create_day_object(date_)
    active_apps = App.objects.filter(is_active=True)
    create_execution_objects(day_object, active_apps)
    executions_due = Execution.objects.filter(day__date=date_, is_due_today=True)

    emails = Message.objects.filter(sent_time__contains=date_)

    for email in emails:
        for execution in executions_due:
            matched = match_email_subject_to_app(email.subject, execution.app)

            if matched is True:
                email.matched_batch_apps = 1
                execution.is_executed = True
                execution.email = email
                execution.save()

            email.processed_batch_apps = 1
            email.save()
