from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import secrets
from todos.todo_controller import crew_controller
from authentication.user_controller import user_controller
from infrastructure.db import db

# Initialize the Flask app
app = Flask(__name__)

# Set up the secret key for session management
app.secret_key = secrets.token_hex(16)

# Configure the SQLAlchemy URI (update as per your environment)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///C:/Users/M iMraN/Desktop/todo-flask-app/test.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy and Flask-Migrate
db.init_app(app)
migrate = Migrate(app, db)

# Register the blueprints for your app
app.register_blueprint(crew_controller)
app.register_blueprint(user_controller)


if __name__ == "__main__":
    app.run(debug=True)
