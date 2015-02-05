Batcher App
===========

A web app based on [Django](https://www.djangoproject.com/), to keep track of executed batch apps using received emails.
Currently developed using Django 1.7 on Python 3.4.

Setup steps for development:

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

7. Go to http://localhost:8000/admin and login using the created admin account

8. Add the mailbox to be monitored in Django_Mailbox app

    ```
    pop3+ssl://email%40domain.com:password@pop.gmail.com
    ```

9. Using the built-in Django admin app, add App to be monitored, along with its frequency and email subject mactching Pattern(s). 

10. (For deployment) In Task Scheduler (Windows) or Crontab (Linux), schedule these tasks within virtualenv session:

    ```
    /path/to/python/ /path/to/batcher/manage.py get_emails_and_process
    ```

    ```
    /path/to/python/ /path/to/batcher/manage.py process_previous_day
    ```
