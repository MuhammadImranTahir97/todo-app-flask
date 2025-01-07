from flask import Flask, render_template, request, session, redirect, Blueprint, jsonify
from infrastructure.db import db
from models.todos import Todo
from flask import request, redirect, url_for, jsonify

crew_controller = Blueprint("crew_bp", __name__)


@crew_controller.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task_content = request.form.get("content")
        if task_content:
            new_task = Todo(content=task_content)
            db.session.add(new_task)
            db.session.commit()

    filter_type = request.args.get("filter", "all")

    if filter_type == "completed":
        tasks = Todo.query.filter_by(completed=True).all()
    elif filter_type == "uncompleted":
        tasks = Todo.query.filter_by(completed=False).all()
    else:
        tasks = Todo.query.all()

    return render_template("index.html", tasks=tasks)


# Delete task
@crew_controller.route("/todos/<int:id>", methods=["POST"])
def delete(id):
    # Check for the _method field in the form data
    if request.form.get("_method") == "DELETE":
        task_to_delete = Todo.query.get(id)
        if not task_to_delete:
            return jsonify({"error": "Task not found!"}), 404

        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            return redirect(
                url_for("crew_bp.index")
            )  # Redirect back to the main page after deleting
        except Exception as e:
            print(e)
            return jsonify({"error": "There was a problem deleting that task"}), 500
    return redirect(url_for("crew_bp.index"))  # Default action if _method is not DELETE


# Update task
@crew_controller.route("/todos/<int:id>", methods=["PATCH"])
def update(id):
    task = Todo.query.get(id)
    if not task:
        return jsonify({"error": "Task not found!"}), 404

    task_content = request.json.get("content")  # Use JSON data for PATCH request
    if not task_content or not task_content.strip():
        return jsonify({"error": "Content is required"}), 400

    task.content = task_content

    try:
        db.session.commit()
        return jsonify({"message": "Task Updated", "task": repr(task)}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "There was an issue updating your task"}), 500


# Get task by ID
@crew_controller.route("/todos/<int:id>", methods=["GET"])
def get_todo(id):
    task = Todo.query.get(id)
    if not task:
        return jsonify({"error": "Task not found!"}), 404
    return jsonify(
        {"id": task.id, "content": task.content, "completed": task.completed}
    )


# Get all tasks
@crew_controller.route("/tasks", methods=["GET"])
def get_todo_all():
    tasks = Todo.query.all()
    task_list = [
        {"id": task.id, "content": task.content, "completed": task.completed}
        for task in tasks
    ]
    return jsonify(task_list), 200


@crew_controller.route("/todos/check_all", methods=["POST"])
def check_all():
    try:
        tasks = Todo.query.all()  # Get all tasks from the database
        for task in tasks:
            task.completed = True  # Mark each task as completed
        db.session.commit()  # Commit changes to the database
        return redirect(
            url_for("crew_bp.index")
        )  # Redirect to the main page after the action
    except Exception as e:
        print(e)
        return (
            jsonify({"error": "There was a problem marking all tasks as completed"}),
            500,
        )


@crew_controller.route("/todos/<int:id>/toggle", methods=["POST"])
def toggle_completed(id):
    task = Todo.query.get(id)
    if not task:
        return jsonify({"error": "Task not found!"}), 404

    task.completed = not task.completed  # Toggle the completed status
    try:
        db.session.commit()
        return redirect(url_for("crew_bp.index"))
    except Exception as e:
        print(e)
        return jsonify({"error": "There was an issue updating your task"}), 500


@crew_controller.route("/todos/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    print(id, "gghf")
    task = Todo.query.get(id)
    if not task:
        return jsonify({"error": "Task not found!"}), 404

    if request.method == "POST":
        task.content = request.form["content"]
        task.completed = "completed" in request.form
        db.session.commit()
        return redirect(url_for("crew_bp.index"))
    return render_template("edit.html", task=task)
