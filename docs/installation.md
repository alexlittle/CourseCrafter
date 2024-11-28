Installation
================

Prerequisites
---------------

* Python 3.11
* Either:
    * Local [Ollama](https://ollama.com/) installed 
    * OpenAI API Key
* Redis server installed 

Installing
------------

# Set up a virtualenv with Python3.11
# run `(venv)$ pip install -r requirements.txt` (this might take some time, there are many packages to install!)
# copy `config/local_settings.py.template` to `config/local_settings.py` and edit to complete your database info and 
  any other specific settings
# in `config/local_settings.py` specify which chat engine and model to use
# run `(venv)$ python manage.py migrate`
# run `(venv)$ python manage.py collectstatic`
# run `(venv)$ python manage.py createsuperuser`


Running
---------

* run Celery worker: (venv)$ celery -A crafter worker --loglevel=info
