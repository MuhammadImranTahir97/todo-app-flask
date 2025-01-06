from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    Blueprint,
    blueprints,
)
import json
from infrastructure.db import db

crew_controller = Blueprint("crew_bp", __name__)


@crew_controller.route("/", methods=["POST"])
def create():
    if request.method == "POST":
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
        except:
            return "There was an issue adding your task"

    return f"Task Created : {new_task}"


@crew_controller.route("/todos/<id>", methods=["DELETE"])
def delete(id):
    task_to_delete = Todo.query.get(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that task"


@crew_controller.route("/todos/<id>", methods=["PATCH"])
def update(id):
    task = Todo.query.get(id)

    if request.method == "POST":
        Todo.content = task("input update task")
        try:
            db.session.commit()
        except:
            return "There was an issue updating your task"


@crew_controller.route("/todos/<id>", methods=["GET"])
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
