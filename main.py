from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:apassword@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

def change_status(task_id):
    
    task = Task.query.get(task_id)

    if task.completed:
        task.completed = False
    else:
        task.completed = True

    db.session.add(task)
    db.session.commit()
    return 


class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.completed = False


@app.route('/', methods = ['POST', 'GET'])
def index():

    if request.method == 'POST':
        task_name = request.form['task']
        new_task = Task(task_name)
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by(completed = False).all()
    completed_tasks = Task.query.filter_by(completed = True).all()

    return render_template('todos.html', title = "Get It Done",
                             tasks=tasks, completed_tasks=completed_tasks)

@app.route("/delete-task", methods =["POST"])
def delete_task():
    task_id = int(request.form["task-id"])
    change_status(task_id)

    return redirect('/')

@app.route("/readd-task", methods =["POST"])
def readd_task():
    task_id = int(request.form["task-id"])
    change_status(task_id)

    return redirect('/')

if __name__ == "__main__":
    app.run()