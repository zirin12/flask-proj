"""
..module:: workerA
  :synopsis:Contains the celery task method that is to be added in the queue

..moduleauthor:: Rahul P <github.com/zirin12>

"""
import os

from . import create_app_celery
from .celery import make_celery
from .models import Task

app = create_app_celery(os.getenv('FLASK_CONFIG') or 'default')
celery_app = make_celery(app)

# celery task in this case is to compute a factorial
@celery_app.task(bind=True)
def add_task(self,num):
    #compute factorial of given number
    fact=1
    for i in range(1,num+1):
        fact = fact * i
    return fact