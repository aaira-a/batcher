from django_mailbox.models import Message
from batch_apps.models import Execution
from batch_apps.generator import get_current_date_in_gmt8
from batch_apps.matcher import match_email_subject_to_app


def execute_end_to_end_tasks(date_=get_current_date_in_gmt8()):
    Execution.objects.generate_and_return_active_apps_execution_objects(date_)
    process_emails(date_)


def process_emails(date_):
    executions_due = get_unexecuted_due_executions(date_)
    emails = get_unprocessed_unmatched_emails(date_)

    for email in emails:
        for execution in executions_due:
            matched = match_email_subject_to_app(email.subject, execution.app)

            if matched is True:
                email.matched_batch_apps = True
                execution.is_executed = True
                execution.email = email
                execution.save()

            email.processed_batch_apps = True
            email.save()


def get_unexecuted_due_executions(date_):
    return Execution.objects.filter(day__date=date_,
                                    is_due_today=True,
                                    is_executed=False)


def get_unprocessed_unmatched_emails(date_):
    return Message.objects.filter(sent_time__year=date_.year,
                                  sent_time__month=date_.month,
                                  sent_time__day=date_.day,
                                  processed_batch_apps=False,
                                  matched_batch_apps=False)
