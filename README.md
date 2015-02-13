[![Build Status](https://travis-ci.org/azam-a/batcher.svg?branch=master)](https://travis-ci.org/azam-a/batcher) [![Coverage Status](https://coveralls.io/repos/azam-a/batcher/badge.svg?branch=master)](https://coveralls.io/r/azam-a/batcher?branch=master)

# Batcher

A web app based on [Django](https://www.djangoproject.com/), to keep track of executed batch apps using email notifications.
Currently developed using Django 1.7 on Python 3.4.

## Background

In our organisation, I was tasked to keep track of executions of batch apps written in various languages and platforms, running on various hosts.

There are daily, weekly and monthly apps to be executed. To check whether the apps were successfully executed, they were designed to send email notifications.

This way, if an email does not arrive as scheduled, some problems could have arisen at the app, network, or mail services level, which requires further investigation. 

Manual checking for each apps proved to be troublesome, even when utilising Google Sheets. Thus, this web app was developed.

## Current Features / Behaviours

- Matching of emails to Apps according to subject field Patterns (content matching is still YAGNI at the moment)
- Using [django_mailbox](https://github.com/coddingtonbear/django-mailbox) package, with a little modifications to the Message model.
- Includes a rough hack to strip email body and SQLite VACUUM command from Message model admin. Needs to be manually triggered.
- Date and time is in GMT+8 context
- Granularity is one day

### Views

```
http://localhost:8000/
http://localhost:8000/executions/
http://localhost:8000/executions/week/
http://localhost:8000/executions/week/yyyy-mm-dd/
http://localhost:8000/executions/day/
http://localhost:8000/executions/day/yyyy-mm-dd/
```

## Why X, Y, Z?

- Django - recently learned how to Python, learning how to Django is a natural progression
- Our production deployment uses nginx, even though not shown in this repository
- SQLite - suits our context, even though not web-scale &trade;
- Why open-source this? - Some poor souls in alternate universes may have the same need and actually thought that this solution would be optimal


## Setup steps:

1. Install Python 3.4, pip, virtualenv and add paths accordingly to system environments

2. In activated virtualenv session, install required packages from requirements.txt

    ```
    pip install -r requirements.txt
    ```

3. On Windows, run patch.bat from /patches/ or do manually the next two steps:

    - Replace admin.py and models.py in django_mailbox installation with the files in /patches/ folder

    - Delete all migrations from django_mailbox installation with the migration files in the /patches/ folder

4. Apply migrations

    ```
    python manage.py migrate
    ```

5. Create an admin

    ```
    python manage.py createsuperuser
    ```

6. Run development server

    ```
    python manage.py runserver
    ```

7. Go to admin panel and login using the created admin account

    ```
    http://localhost:8000/admin
    ```

8. Add the mailbox to be monitored in Django_Mailbox app

    ```
    pop3+ssl://email%40domain.com:password@pop.gmail.com
    ```

9. Using the built-in Django admin app, add App to be monitored, along with its frequency and email subject mactching Pattern(s)

10. (For deployment) In Task Scheduler (Windows) or Crontab (Linux), schedule these tasks within virtualenv session, perhaps once an hour:

    ```
    /path/to/python/ /path/to/batcher/manage.py get_emails_and_process
    ```

    ```
    /path/to/python/ /path/to/batcher/manage.py process_previous_day
    ```

11. Use the implemented views to see the execution status of the Apps
