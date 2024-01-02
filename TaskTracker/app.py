from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task (db.Model):
    task_num = db.Column(db.Integer,primary_key=True)
    task_name = db.Column(db.String(100))
    task_complete = db.Column(db.Boolean)

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html',tasks = tasks)

@app.route('/add',methods=['POST'])
def add():
    task_name = request.form.get("task_name")
    new_task = Task(task_name=task_name, task_complete=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/update/<int:task_num>')
def update(task_num):
    task = db.session.get(Task, task_num)
    task.task_complete = not task.task_complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/delete/<int:task_num>')
def delete(task_num):
    task = db.session.get(Task, task_num)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)