How to run this Django Server ? 
=================================

### Requirements :
- Python 3.6 or latest (you can try with Python 3.5, not sure if it works)
    --> if you are not sure which version of Python is called by default : 
        CMD : python -v
- Django 1.11 (really needed)
    --> CMD : pip install django
- Django Rest Framework (really needed too)
    --> CMD : pip install django-rest-framework
- Django Cors Headers (really needed too)
    --> CMD : pip install django-cors-headers

### To Run the server :


__If you already have an older version :__
- Delete db.sqlite3, and every files in migrations folder except __init__.py

__Else :__
- Open a shell in the django project root directory (which contains a file manage.py)
- CMD : python manage.py makemigrations
- CMD : python manage.py migrate
- CMD : python manage.py loaddata dump.json
- CMD : python manage.py runserver
At this point, the server is running on localhost:8000. Try to make a request with your browser.