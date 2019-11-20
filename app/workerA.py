"""
.. module:: workerA
  :synopsis: Contains the celery task method that is to be added in the queue

.. moduleauthor:: Rahul P <github.com/zirin12>

"""
import os

from . import create_app_celery
from .celery import make_celery
from .models import Task

# create a celery app instance to define tasks
app = create_app_celery(os.getenv('FLASK_CONFIG') or 'default')
celery_app = make_celery(app)

# celery task in this case is to compute a factorial
@celery_app.task(bind=True)
def add_task(self,num):
    """
      **Compute factorial of a number passed as the argument**

            This function(task) allows users to call the task to compute the factorial of a given number 
            
            :param: number
            :return: Async result object which has the factorial or result stored
    """
    #compute factorial of given number
    fact=1
    for i in range(1,num+1):
        fact = fact * i
    return fact