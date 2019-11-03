from flask import Flask,jsonify,make_response
from celery import Celery, states
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/task/<number>',methods=['POST'])
def task(number):
    fact = compute_factorial.apply_async(args=[number])
    return make_response(jsonify({'task_id': fact.fact_id}))

@celery.task(bind=True)
def compute_factorial(self,number):
    self.update_state(state=states.PENDING)
    factorial=1
    for i in range(1,number+1):
        factorial = factorial*i
    return factorial

@app.route('/task/<task_id>', methods=['GET'])
def check_task_status(task_id):
    task = compute_factorial.AsyncResult(task_id)
    state = task.state
    response = {}
    response['state'] = state

    if state == states.SUCCESS:
        response['result'] = task.get()
    elif state == states.FAILURE:
        try:
            response['error'] = task.info.get('error')
        except Exception as e:
            response['error'] = 'Unknown error occured'
    
    return make_response(jsonify(response))

if __name__ == '__main__':
    app.run(debug=True)