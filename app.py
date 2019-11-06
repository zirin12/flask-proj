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
def add():
    number = request.args.get('number')
    result = add_task.delay(int(number))
    task = Task(result.task_id,False)
    db.session.add(task)
    db.session.commit()
    return jsonify({'result':result.task_id}), 200

@app.route("/task_status",methods=['GET', 'POST'])
def subtract():
    task_id = request.args.get('task_id')
    update_db.delay(task_id,'sqlite:///tasks.sqlite3')
    task = Task.query.get(task_id)
    #print(task.processed)
    return jsonify({'result': task.processed}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)