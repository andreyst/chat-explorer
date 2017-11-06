# Installation

1. Clone this repo from github
2. Install necessary python libraries:
```
pip3 install Django==1.11.6 telethon celery django-celery-results "celery[redis]" pytz tzlocal
```
3. Copy settings
```
$ cd chat-explorer/chatexplorer
$ cp local_settings.py.example local_settings.py
```
4. Get your api settings from https://my.telegram.org/ and put them in local_settings.py
5. Install redis for celery (if you have RabbitMQ or SQS available, you can use them instead for celery backend). You can install it locally or use included docker-compose.yml
6. (Optional) Use your existing db for django installation. By default it uses sqlite database.
7. Run all the components (currently this app is supposed to be run locally for your own chats)
```
$ docker-compose up -d
Starting chatexplorer_redis_1 ...
Starting chatexplorer_redis_1 ... done

$ celery -A chatexplorer worker -l info
(...celery will run in foreground)

$ python3 manage.py runserver
(...django dev server will run in foreground)
```

# Usage

1. Open app: http://localhost:8000/
2. Add messenger account (currently Telegram only)
3. Import the chat from the account
