import json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


# Define the Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)  # Optional
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Automatically set
    updated_task = db.Column(db.DateTime)
