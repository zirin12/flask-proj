# flask-proj

## Flask project using celery backed distributed task queue and redis as a message broker.

## Description

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


## Build and launch using docker
```
docker-compose up -d --build
```
This will expose the Flask application's endpoints on port 5001 
To add more workers:
```
docker-compose up -d --scale worker=5 --no-recreate
```
To shut down:
```
docker-compose down
```
To change the endpoints, update the code in api/app.py
 
 
Example docker-compose config for scaling celery worker with separate code base. It uses the classical addition task as an example. flask-app and flask-celery have seperate codebase (In other words we don't need to have access to the celery task module and don't need to import the celery task in the flask app) and flask-app uses the name attribute of a task and celery.send_task to submit a job without having the access to celery workers code base.
To run the example:
docker-compose build
docker-compose up -d # run in detached mode
 
Now load http://your-dockermachine-ip:5000/add/2/3 in browser. It should create a task and return a task id.
To check the status of the job hit http://your-dockermachine-ip:5000/check/taskid. It should either show PENDING or the result 5.
To monitor that the worker is working fine go to http://your-dockermachine-ip:5555.It runs a flower server. It should show one worker ready to serve.
To scale the workers, now run docker-compose scale worker=5. This will create 4 more containers each running a worker. http://your-dockermachine-ip:5555 should now show 5 workers waiting for some jobs!
