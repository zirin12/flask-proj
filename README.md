# flask-proj

### Note : The other branch explores a different way of calling the update task

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
6. Alternatively instead of running the above commands , you can run the bash files in order .

```
    ./run-redis.sh
    ./run-workerA.sh
    ./run-workerB.sh
    ./run-flask.sh 
    ./run-migrate.sh
``` 

7. Go to http://localhost:5000/ and you can see the page with the swagger documentation . Go to apis under tasks and you can see the two endpoints which you can try with inputs.


## Build and launch using docker
Run the following commands in the project directory.
```
docker-compose up -d --build
```

This will expose the Flask application's endpoints on port 5000

To add more workers:
```
docker-compose up -d --scale worker=4 --no-recreate
```

-d is to run in detached mode

To shut down:
```
docker-compose down
```
To change the endpoints, update the code in api/app.py
 
* Now load http://your-dockermachine-ip:5000 in browser.You can see the page listing the task api and other swagger information . When you click on the task api bar you 'll see two endpoints , One for adding tasks(POST api) and the other for getting task status (GET api)

* The POST api lets you create a task and in response after adding one you'll get the task id . This task id is then passed to the GET api for getting the task status. You might have to keep doing GET requests to know the updated status because celery tasks run in the background

* To check the status of the job hit http://your-dockermachine-ip:5000/task/<taskid>. It should either show PENDING or SUCCESS with the result
    
* To scale the workers, now run docker-compose scale worker=5. This will create 4 more containers each running a worker.

To take a look at the docker logs , first run the following command :

```
docker-compose ps
```

On the left column you can see the individual names of wach container

To access the logs of each service , run :

```
docker logs < Container name > -f --tail=50 # tail=50 gives the last 50 lines of the log

````


