"""
.. module:: celery
  :synopsis: Helps to create a Celery app instance with configurations which can then be imported in other modules.
"""

from celery import Celery

def make_celery(app):
    """
        **Make a celery app instance and return it with app context passed as parameter**

            This function allows users to create celery app instances in their module with the app context
            to define celery tasks and other functions.
            
            :param: current app
            :return: Celery instance
    """
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery