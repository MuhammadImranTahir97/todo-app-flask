from flask import Flask, render_template, request, session, redirect, Blueprint
from infrastructure.db import db
from models.todos import Todo


# Assuming Todo model is defined somewhere
# from your_model_file import Todo

crew_controller = Blueprint("crew_bp", __name__)


@crew_controller.route("/", methods=["POST"])
def create():
    task_content = request.form.get("content")  # Assuming form data has 'content' field
    new_task = Todo(content=task_content)

    try:
        db.session.add(new_task)
        db.session.commit()
        return f"Task Created: {new_task}"
    except:
        return "There was an issue adding your task"


@crew_controller.route("/todos/<int:id>", methods=["DELETE"])
def delete(id):
    task_to_delete = Todo.query.get(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that task"


@crew_controller.route("/todos/<int:id>", methods=["PATCH"])
def update(id):
    task = Todo.query.get(id)
    if not task:
        return "Task not found!"

    task_content = request.form.get("content")  # Assuming form data has 'content' field
    task.content = task_content

    try:
        db.session.commit()
        return f"Task Updated: {task}"
    except:
        return "There was an issue updating your task"


@crew_controller.route("/todos/<int:id>", methods=["GET"])
def get_todo(id):
    task = Todo.query.get(id)
    if not task:
        return "Task not found!"
    return f"Task ID: {task.id}, Content: {task.content}, Completed: {task.completed}"


@crew_controller.route("/", methods=["GET"])
def get_todo_all():
    tasks = Todo.query.all()
    return "<br>".join(
        [
            f"ID: {task.id}, Content: {task.content}, Completed: {task.completed}"
            for task in tasks
        ]
    )
