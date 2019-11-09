import sqlalchemy
from sqlalchemy.orm import sessionmaker
from celery import Celery
from celery.result import AsyncResult
from models import Task,db

# Celery configuration
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

#Initialize Celery
celery = Celery('workerB',broker=CELERY_BROKER_URL,backend = CELERY_RESULT_BACKEND)

def connect(uri):
    """Connects to the database and return a session"""

    uri = uri

    con = sqlalchemy.create_engine(uri)

    Session = sessionmaker(bind=con)
    session = Session()

    return con, session

@celery.task()
def update_db(task_id, uri):
    con, session = connect(uri)
    res = AsyncResult(task_id)
    print(res.ready())
    if res.ready():
        task = session.query(Task).get(task_id)
        task.processed = True
        session.commit()
