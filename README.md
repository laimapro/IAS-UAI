# IAS Django

## Setup


The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/paulo4ndre/ias.git
$ cd ias
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ pip install virtualenv
```
On Windows:
```sh
$ virtualenv venv
$ cd venv/scripts
$ activate
```
On Linux:
```sh
$ virtualenv venv
$ source venv/bin/activate
```

Then install the dependencies (in the project root folder):
```sh
(venv)$ pip install -r requirements-dev.txt
```

Install database dependencies:
```sh
(venv)$ python manage.py migrate
```

Load table presets (Fixtures)
```sh
(venv)$ python manage.py loaddata loadfixtures
```

Create admin user:
```sh
(venv)$ python manage.py createsuperuser
```

Run project:
```sh
(venv)$ python manage.py runserver
```


Type in your browser http://localhost:8000/

