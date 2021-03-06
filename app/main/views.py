from datetime import date
from flask import (g, render_template, abort, request, make_response, jsonify)
from flask_httpauth import HTTPBasicAuth

from . import main
from .. import db
from ..models import Todo, User

# will be used for restful authentication
auth = HTTPBasicAuth()


def _get_todo_or_404(user: User, uuid: str) -> Todo:
    """
    Helper function that returns a Todo based on the user and the
    exposed ID
    """
    todo_item = (Todo.query
                 .filter_by(user=user, uuid=uuid)
                 .scalar())
    if not todo_item:
        abort(404)
    return todo_item


# following function is a basic method for handling authentication.
# it is used for RESTful services and tests if the user provides a password
# that, when hashed, matches the hash of a previously provided password
# users can POST to the /todos/api/v1.0/users endpoint to create a new user

@auth.verify_password
def verify_password(username, password):
    """
    verify user comparing hash of provided password with previously
    computed hash
    """
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@auth.error_handler
def unauthorized():
    """return JSON indicating unauthorized access"""
    return make_response(jsonify({'error': 'unauthorized Access'}), 401)


# these are the endpoints for the web front end
@main.route('/', methods=['GET'])
@main.route('/todos/', methods=['GET'])
@auth.login_required
def index():
    """ index is the home page of the Todo Application """
    return render_template('index.html')


# These are the RESTful services (GET, PUT, POST, DELETE)
@main.route('/todos/api/v1.0/user/create', methods=['POST'])
def new_user():
    """Create user"""
    username = request.json.get('username')
    password = request.json.get('password')
    if (username is None or password is None or
            User.query.filter_by(username=username).first() is not None):
        abort(400)
    user = User(username, password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': username}), 201


@main.route('/todos/api/v1.0/todos', methods=['GET'])
@auth.login_required
def get_todos():
    """RESTful getting the entire todos"""
    todos = Todo.query.filter_by(user=g.user).all()
    return jsonify({'todos': [todo.to_json() for todo in todos]}), 200


@main.route('/todos/api/v1.0/todo/<string:uuid>', methods=['GET'])
@auth.login_required
def get_todo(uuid):
    """RESTful getting a todo"""
    todo_item = _get_todo_or_404(g.user, uuid)
    return jsonify(todo_item.to_json()), 200


@main.route('/todos/api/v1.0/todo/create', methods=['POST'])
@auth.login_required
def create_todo():
    """RESTful creating a todo"""
    if not request.json:
        abort(400)
    print(type(request.json))
    todo = Todo.from_json(request.json)
    todo.user = g.user
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_json()), 201


@main.route('/todos/api/v1.0/todo/update/<string:uuid>', methods=['PUT'])
@auth.login_required
def update_todo(uuid):
    """RESTful updating a todo"""
    if not request.json:
        abort(400)
    todo_item = _get_todo_or_404(g.user, uuid)
    todo_item.title = request.json.get('title', todo_item.title)
    todo_item.body = request.json.get('body', todo_item.body)
    todo_item.priority = request.json.get('priority', todo_item.priority)
    todo_item.done = request.json.get('done', todo_item.done)
    todo_item.date_ = request.json.get('date', todo_item.date)
    todo_item.category = request.json.get('category', todo_item.category)
    db.session.add(todo_item)
    db.session.commit()
    return jsonify(todo_item.to_json()), 200


@main.route('/todos/api/v1.0/todo/delete/<string:uuid>', methods=['DELETE'])
@auth.login_required
def delete_todo(uuid):
    """RESTFUL deleting a todo"""
    if not request.method == 'DELETE':
        abort(400)
    todo_item = _get_todo_or_404(g.user, uuid)
    db.session.delete(todo_item)
    db.session.commit()
    return jsonify({'result': 'Todo deleted.'}), 200
