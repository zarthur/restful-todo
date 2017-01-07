from uuid import uuid4

import bcrypt

from app import db
from exceptions import ValidationError


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column(db.String)
    password_hash = db.Column(db.String)
    contacts = db.relationship("Contact", back_populates="user")

    def __init__(self, username: str, password: str):
        self.username = username
        self.hash_password(password)

    def hash_password(self, password: str):
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def verify_password(self, password: str) -> bool:
        hashed = bcrypt.hashpw(password.encode(), self.password_hash)
        return self.password_hash == hashed


class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User")
    name = db.Column(db.String)
    email = db.Column(db.String)
    favorite = db.Column(db.Boolean)
    address = db.Column(db.String)
    uuid = db.relationship(db.String)

    def __init__(self, name: str, email: str, address: str,
                 favorite: bool = False, uuid: str = None):
        self.uuid = uuid or str(uuid4())
        self.name = name
        self.email = email
        self.address = address
        self.favorite = favorite

    @staticmethod
    def from_json(json_post):
        name = json_post.get('name')
        email = json_post.get('email')
        address = json_post.get("address")
        favorite = json_post.get("favorite", False)
        uuid = json_post.get("uuid", str(uuid4()))
        if name is None or name == '':
                raise ValidationError('post does not have a name')
        return Todo(name, email, address, favorite, uuid)

    def to_json(self):
        todo_json = {
            'name': self.name,
            'email': self.email,
            'address': self.address,
            'favorite': self.favorite,
            'uuid': self.uuid
        }
        return todo_json

    def __repr__(self):
        return "<Contact {name}>".format(name=self.name)

