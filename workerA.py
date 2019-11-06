from celery import Celery

# Celery configuration
CELERY_BROKER_URL = 'amqp://rahul:rahul123@localhost:5672/myvhost'
CELERY_RESULT_BACKEND = 'amqp'

#Initialize Celery
celery = Celery('workerA', broker=CELERY_BROKER_URL,backend = CELERY_RESULT_BACKEND)

@celery.task()
def add_task(num):
    #compute factorial of given number
    fact=1
    for i in range(1,num+1):
        fact = fact * i
    return fact