# flask-proj

## Flask project using celery backed distributed task queue and redis as a message broker.

### Description

This project uses the flask micro web framework with flask restplus for defining rest endpoints, This flask applications acts like a celery client to submit tasks and get updates from the celery workers. Redis is used as the message broker to communicate with the workers to know their status and mediate them.
Nginx is used a frontend reverse proxy to route requests to the uWSGI application server running the flask application.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

1. Clone this repository.
```
    git clone https://github.com/zirin12/flask-proj.git
```
2. Create a virtualenv and install the requirements.
```
    python3 -m venv env
    source venv/bin/activate
    pip install -r requirements.txt
```
3. Open a second terminal window and start a local Redis server (if you are on Linux or Mac, execute run-redis.sh to install and launch a private copy).

    #### Linux\MacOS
```
    chmod +x run-redis.sh
    ./run-redis.sh or sh run-redis.sh 
```

4. Open a third terminal window. Set two environment variables FLASK_APP and FLASK_ENV to manage.py and development respectively. (This is done to run the flask app). Then start the two celery workers i.e,workerA and workerB in two different terminals.

``` 
    export FLASK_APP=manage.py
    export FLASK_ENV=development
```
  
```
    celery -A app.workerA.celery_app worker --loglevel=info -Q workerA
```
 
```
    celery -A app.workerB.celery_app worker --loglevel=info -Q workerB
```
5. Run the database migrations and then run the flask application
```
    flask db init
    flask db migrate
    flask db upgrade
```
```
    flask run
```
  
6. Go to http://localhost:5000/ and you can see the page with the swagger documentation . Go to apis under tasks and you can see the two endpoints which you can try with inputs.
