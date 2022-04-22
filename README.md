# Banking App

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/hyderanees/banking_tranfer_app.git
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd banking_tranfer_app
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.

## Walkthrough

Before you interact with the application, go to `.env` file in root directory and 
change `ALLOWED_HOSTS`, `DJANGO_DEBUG`, `CORS_ORIGIN_WHITELIST`.

Following are the urls available

1. `http://127.0.0.1:8000/api/register/` Method `POST`
2. `http://127.0.0.1:8000/api/login/` Method `POST`
3. `http://127.0.0.1:8000/bank/` Method `POST` & `GET`
4. `http://127.0.0.1:8000/account/` Method `POST` & `GET`
5. `http://127.0.0.1:8000/account/add_money_in_account/` Method `POST`
6. `http://127.0.0.1:8000/account/send_money_from_one_account_to_another/` Method `POST`
`project/gc_app/views.py` in the `webhook_data` variable.
