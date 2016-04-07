import bcrypt

from datetime import datetime
from . import db
from app.exceptions import ValidationError


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    todos = db.relationship("Todo", back_populates="owner")

    def __init__(self, username: str, password: str):
        self.username = username
        self.set_password(password)

    def set_password(self, new_password: str):
        self.password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())

    def verify_password(self, password: str) -> bool:
        hashed = bcrypt.hashpw(password.encode(), self.password.encode())
        return self.password.encode() == hashed


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column('id', db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    owner = db.relationship("User")
    title = db.Column(db.String(50))
    body = db.Column(db.String)
    done = db.Column(db.Boolean)
    publication_date = db.Column(db.DateTime)

    def __init__(self, owner: User, title: str, body: str):
        self.owner = owner
        self.title = title
        self.body = body
        self.done = False
        self.publication_date = datetime.utcnow()

    @staticmethod
    def from_json(json_post):
        title = json_post.get('title')
        body = json_post.get('body')
        if body is None or body == '':
                raise ValidationError('post does not have a body')
        return Todo(title,body)

    def to_json(self):
        todo_json = {
                        'id' : self.id,
                        'title' : self.title,
                        'body' : self.body,
                        'done' : self.done
        }
        return todo_json

    def __repr__(self):
        return "<Todo '%s'>" % self.title

