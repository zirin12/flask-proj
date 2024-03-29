"""
.. module:: models
  :synopsis: Contains model of a Task Record

.. moduleauthor:: Rahul P <github.com/zirin12>

"""
from . import db

# class Task defining each attribute of a task
class Task(db.Model):
    """Model for storing tasks."""

    task_id = db.Column(db.String,primary_key=True)
    status = db.Column(db.String)
    result = db.Column(db.Integer,nullable=True)

    def __init__(self,task_id,status,result=None):
        self.task_id = task_id
        self.status = status
        self.result = result