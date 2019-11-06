from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    """Model for storing tasks."""

    task_id = db.Column(db.String,primary_key=True)
    processed = db.Column(db.Boolean)

    def __init__(self,task_id,processed):
        self.task_id = task_id
        self.processed = processed
