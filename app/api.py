"""
.. module:: api
  :synopsis: Endpoints for adding a task and retreiving the task status are defined here

.. moduleauthor:: Rahul P <github.com/zirin12>

"""

from flask_restplus import Api, Resource, fields, abort
from .workerA import add_task
from .workerB import update_db
from . import models, db
from sqlalchemy.orm.exc import NoResultFound

api = Api(
    version = '1.0',
    title='TASK_API',
    description='task_api',
)

ns = api.namespace('api', description='task api namespace')

def add_task_db(task_id):
    """ 
        **Save Task to database**

        This saves the task to the task table in the database.
    """
    task = models.Task(task_id,"PENDING")
    db.session.add(task)
    db.session.commit()

    return task

task_response_model = api.model('task_response', {
    "task_id": fields.String(description="task_id", required=True),
    "status": fields.String(description="task status", required=True),
    "result": fields.Integer(description="Factorial of the number"),
})

task_request_model = api.model('task_request', {
    "number": fields.Integer,
})


@ns.route('/tasks')
class TaskNew(Resource):
    @api.doc(responses={
        201: 'Task is started',
        400: 'Validation Error',
    })
    @api.expect(task_request_model, validate=True)
    @api.marshal_with(task_response_model, code=201)
    def post(self):
        """
            **Add a Task (Factorial of a number) in the queue and save in database**

            This function allows users to create a task to compute the factorial of a given number 

            :return: Task's information in json and http status code

            - Example::

                    curl -X POST "http://localhost:5000/api/tasks" -H "accept: application/json" -H "Content-Type: application/json" \
                        -d "{ 
                            "number": 4
                        }"
            
            - Expected Success Response::

                HTPP Status Code: 201

                {
                    "task_id": "778adfbc-5b28-4e27-b00c-a6438e073220",
                    "status": "PENDING"
                }
            
            - Expected Fail Response::
    
        """
        number = api.payload["number"]
        if number <= 0 :
            abort(400, "number should be greater than zero",number=number)
        # number = int(number)
        result = add_task.apply_async((number,),queue='workerA')
        task = add_task_db(result.task_id)

        return task,201


@ns.route('/tasks/<task_id>')
class TaskStatus(Resource):
    
    @api.doc('get task status')
    @api.marshal_with(task_response_model, code=200)
    def get(self, task_id):
        """
            **Get task status (PENDING or COMPLETED) given the task id**

            This function allows user to get the status of a task already submitted given it's task_id.

            :param task_id: id of the task 
            :type task_id: String
            :return: task's status information in json and http status code

            - Example::

                    curl -X GET "http://localhost:5000/api/tasks/778adfbc-5b28-4e27-b00c-a6438e073220" -H "accept: application/json"

            - Expected Success Response::

                HTTP Status Code: 200

                {
                    "task_id": "778adfbc-5b28-4e27-b00c-a6438e073220",
                    "status": "SUCCESS"
                }

            - Expected Fail Response::
        """
        try:
            update_db.apply_async((task_id,),queue='workerB')
            task = db.session.query(models.Task).filter_by(task_id = task_id).one()
        except NoResultFound:
            abort(400,"Given task id does not exist in database",task_id=task_id)

        return task,200
