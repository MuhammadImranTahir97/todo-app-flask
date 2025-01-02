from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# print(os.getcwd())

# Initialize the Flask app and the database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///C:/Users/M iMr][paN/Desktop/todo-flask-app/test.db"
)
db = SQLAlchemy(app)


# Define the Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)  # Optional
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Automatically set
    updated_task = db.Column(db.DateTime)


def __repr__(self):
    return f"<ID {self.id}: Task: {self.content}, Completed: {self.completed}>"


@app.route("/create", methods=["POST"])
def create():
    if request.method == "POST":
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
        except:
            return "There was an issue adding your task"

    return f"Task Created : {new_task}"


@app.route("/delete/<id>")
def delete(id):
    task_to_delete = Todo.query.get(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that task"


@app.route("/update/<id>", methods=["POST"])
def update(id):
    task = Todo.query.get(id)

    if request.method == "POST":
        Todo.content = task("input update task")
        try:
            db.session.commit()
        except:
            return "There was an issue updating your task"


@app.route("/get-todo/<id>")
def get_todo(id):
    task = Todo.query.get(id)
    if not task:
        return "Task not found!"
    return f"Task ID: {task.id}, Content: {task.content}, Completed: {task.completed}"


@app.route("/get-todo-all")
def get_todo_all():
    tasks = Todo.query.all()
    return "<br>".join(
        [
            f"ID: {task.id}, Content: {task.content}, Completed: {task.completed}"
            for task in tasks
        ]
    )


# Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
