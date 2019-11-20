"""
.. module:: workerB
   :synopsis: Contains the celery task which is responsible for updating the status of task in workerA in the database

.. moduleauthor:: Rahul P <github.com/zirin12>
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
    """
        **Get the task status with task id and update in database**

            This function allows users to run an update task on the task with given task id and uses asyncresult call to know 
            the task state if it's completed or pending .Based on the present state it accordingly
            updates in database. 

            :param: task id
            :return: Async result object
    """
    res = AsyncResult(task_id)
    #print(res.ready())
    #if res.ready():
    task = db.session.query(Task).get(task_id)
    task.status = res.status
    if res.ready() :
        task.result = res.result
    db.session.commit()