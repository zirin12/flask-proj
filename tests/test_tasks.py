from app.workerA import add_task
from app.workerB import update_db
from app.models import Task

def test_add_task(session,celery_worker):
    task = add_task.apply((4,))
    assert task.result == 24
    assert task.status == "SUCCESS"

def test_update_db(session,celery_worker):
    task = add_task.apply((5,))
    response = update_db(task.task_id)
    assert response.result == 120
    assert response.status == "SUCCESS"
    task_record = session.query(Task).filter_by(task_id = task.task_id).one()
    assert task.result == 120
    assert task.status == "SUCCESS"
