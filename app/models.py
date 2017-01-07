from uuid import uuid4

import bcrypt

from app import db
from exceptions import ValidationError


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
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User")
    title = db.Column(db.String(50))
    body = db.Column(db.String)
    done = db.Column(db.Boolean)
    priority = db.Column(db.Integer)
    uuid = db.relationship(db.String)

    def __init__(self, title: str, body: str, priority: int,
                 done: bool = False, uuid: str = None):
        self.uuid = uuid or str(uuid4())
        self.title = title
        self.body = body
        self.done = done
        self.priority = priority

    @staticmethod
    def from_json(json_post):
        title = json_post.get('title')
        body = json_post.get('body')
        priority = json_post.get("priority")
        done = json_post.get("done", False)
        uuid = json_post.get("uuid", str(uuid4()))
        if body is None or body == '':
                raise ValidationError('post does not have a body')
        return Todo(title, body, priority, done, uuid)

    def to_json(self):
        todo_json = {
            'title': self.title,
            'body': self.body,
            'done': self.done,
            'priority': self.priority,
            'uuid': self.uuid
        }
        return todo_json

    def __repr__(self):
        return "<Todo {title}>".format(title=self.title)

