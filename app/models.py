import bcrypt

from datetime import datetime
from . import db
from app.exceptions import ValidationError
from sqlalchemy import func


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column(db.String)
    password_hash = db.Column(db.String)
    todos = db.relationship("Todo", back_populates="user")

    def __init__(self, username: str, password: str):
        self.username = username
        self.hash_password(password)

    def hash_password(self, password: str):
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def verify_password(self, password: str) -> bool:
        hashed = bcrypt.hashpw(password.encode(), self.password_hash)
        return self.password_hash == hashed


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column('id', db.Integer, primary_key=True)
    user_exposed_id = db.Column('user_exposed_id', db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User")
    title = db.Column(db.String(50))
    body = db.Column(db.String)
    done = db.Column(db.Boolean)
    publication_date = db.Column(db.DateTime)

    def __init__(self, user: User, title: str, body: str):
        previous_id = Todo.query.with_entities(func.max(Todo.user_exposed_id)).filter(Todo.user_id == user.id).scalar()
        self.user_exposed_id = previous_id + 1 if previous_id is not None else 0
        print("USER EXPOSED ID: " + str(self.user_exposed_id))
        self.title = title
        self.body = body
        self.done = False
        self.publication_date = datetime.utcnow()

    @staticmethod
    def from_json(user, json_post):
        title = json_post.get('title')
        body = json_post.get('body')
        if body is None or body == '':
                raise ValidationError('post does not have a body')
        return Todo(user, title, body)

    def to_json(self):
        todo_json = {
            'id' : self.user_exposed_id,
            'title' : self.title,
            'body' : self.body,
            'done' : self.done
        }
        return todo_json

    def __repr__(self):
        return "<Todo {title}>".format(title=self.title)

