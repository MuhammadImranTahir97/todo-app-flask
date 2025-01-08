from datetime import datetime
from infrastructure.db import db


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)  # Optional
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Automatically set
    updated_task = db.Column(db.DateTime)

    # Add user_id to link the Todo to a User
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # Define the relationship to User
    user = db.relationship("User", back_populates="todos")

    def __repr__(self):
        return f"<ID {self.id}: Task: {self.content}, Completed: {self.completed}>"

    def update_task(self, new_content=None, new_completed=None):
        if new_content:
            self.content = new_content
        if new_completed is not None:
            self.completed = new_completed
        self.updated_task = datetime.utcnow()
