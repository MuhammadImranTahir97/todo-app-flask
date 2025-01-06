from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from infrastructure import db
from routes.controllers import crew_controller

# Initialize the Flask app and the database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///C:/Users/M iMraN/Desktop/todo-flask-app/test.db"
)


app.register_blueprint(crew_controller)

if __name__ == "__main__":
    app.run(debug=True)
