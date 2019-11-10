from flask_restplus import Api, Resource, fields, abort
from .workerA import add_task
from .workerB import update_db
from . import models, db

api = Api(
    version = '1.0',
    title='TASK_API',
    description='task_api',
)

ns = api.namespace('api', description='task api namespace')

def add_task_db(task_id):
    task = models.Task(task_id,False)
    db.session.add(task)
    db.session.commit()

    return task

task_response_model = api.model('task_response', {
    "task_id": fields.String(description="task_id", required=True),
    "processed": fields.Boolean(description="task status", required=True),
})

task_request_model = api.model('task_request', {
    "number": fields.Integer,
})


@ns.route('/tasks')
class TaskNew(Resource):
    @api.doc(responses={
        201: 'Task is started',
    })
    @api.expect(task_request_model, validate=True)
    @api.marshal_with(task_response_model, code=201)
    def post(self):
        number = api.payload["number"]
        # number = int(number)
        result = add_task.apply_async((number,),queue='workerA')
        task = add_task_db(result.task_id)

        return task,201


@ns.route('/tasks/<task_id>')
class TaskStatus(Resource):
    @api.doc('get task status')
    @api.marshal_with(task_response_model, code=200)
    def get(self, task_id):
        update_db.apply_async((task_id,),queue='workerB')
        task = db.session.query(models.Task).filter_by(task_id = task_id).one()

        return task,200
