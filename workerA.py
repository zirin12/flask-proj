from celery import Celery

# Celery configuration
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

#Initialize Celery
celery = Celery('workerA', broker=CELERY_BROKER_URL,backend = CELERY_RESULT_BACKEND)

@celery.task()
def add_task(num):
    #compute factorial of given number
    fact=1
    for i in range(1,num+1):
        fact = fact * i
    return fact