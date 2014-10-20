Batcher App
===========

A web app based on [Django](https://www.djangoproject.com/), to keep track of executed batch apps using received emails.
Currently developed using Django 1.7 on Python 3.4.

Setup steps for development:

- Install Python 3.4 & pip, add paths accordingly

- Install Django package from PyPI

```
pip install django
```

- Install [django_mailbox](https://github.com/coddingtonbear/django-mailbox) package from PyPI

```
pip install django_mailbox
```

- Apply migrations from project folder

```
python manage.py migrate
```

- Run development server

```
python manage.py runserver
```

- Create an admin

```
python manage.py createsuperuser
```

- Add a development mailbox in Django_Mailbox app

```
pop3+ssl://email%40domain.com:password@pop.gmail.com
```
