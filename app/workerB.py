import os

from . import create_app_celery, db
from celery.result import AsyncResult
from .celery import make_celery
from .models import Task

app = create_app_celery(os.getenv('FLASK_CONFIG') or 'default')
celery_app = make_celery(app)


@celery_app.task()
def update_db(task_id):
    #con, session = connect(uri)
    res = AsyncResult(task_id)
    #print(res.ready())
    #if res.ready():
    task = db.session.query(Task).get(task_id)
    task.processed = res.ready()
    db.session.commit()