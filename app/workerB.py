"""
.. module:: workerB
   :synopsis: Contains the celery task which is responsible for updating the status of task in workerA in the database

..moduleauthor:: Rahul P <github.com/zirin12>
"""

import os

from . import create_app_celery, db
from celery.result import AsyncResult
from .celery import make_celery
from .models import Task

app = create_app_celery(os.getenv('FLASK_CONFIG') or 'default')
celery_app = make_celery(app)

# Celery task that gets the status of the task whose task id is given and updates the status in database
@celery_app.task()
def update_db(task_id):
    res = AsyncResult(task_id)
    #print(res.ready())
    #if res.ready():
    task = db.session.query(Task).get(task_id)
    task.processed = res.ready()
    db.session.commit()