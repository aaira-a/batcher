Batcher App
===========

A web app based on [Django](https://www.djangoproject.com/), to keep track of executed batch apps using received emails.
Currently developed using Django 1.7 on Python 3.4.

Setup steps for development:

- Install Python 3.4, pip, virtualenv and add paths accordingly

- In virtualenv session, install required packages from requirements.txt

```
pip install -r requirements.txt
```

- Replace admin.py and models.py in django_mailbox installation from requirements.txt with the files in /patches/ folder

- Delete all migrations from django_mailbox installation from requirements.txt with the migration files in the /patches/ folder

- Apply migrations

```
python manage.py migrate
```

- Create an admin

```
python manage.py createsuperuser
```

- Run development server

```
python manage.py runserver
```

- Add a development mailbox in Django_Mailbox app

```
pop3+ssl://email%40domain.com:password@pop.gmail.com
```
