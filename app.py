from workerA import add_task
from workerB import update_db
from models import db,Task
from flask import (
    Flask,
    jsonify,
    request,
)

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.sqlite3'
db.init_app(app)

@app.route("/add_task",methods=['GET', 'POST'])
def add_task():
    number = request.args.get('number')
    number = int(number)
    result = add_task.apply_async((number,),queue='workerA')
    task = Task(result.task_id,False)
    db.session.add(task)
    db.session.commit()
    return jsonify({'result':result.task_id}), 200

@app.route("/task_status",methods=['GET', 'POST'])
def task_status():
    task_id = request.args.get('task_id')
    update_db.apply_async((task_id,'sqlite:///tasks.sqlite3',),queue='workerB')
    task = Task.query.get(task_id)
    #print(task.processed)
    return jsonify({'result': task.processed}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(host='0.0.0.0')