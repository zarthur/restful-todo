from flask import (g, render_template, redirect, url_for, abort, flash,
                   request, make_response, jsonify)
from flask_httpauth import HTTPBasicAuth

from . import main
from .. import db
from ..models import Contact, User

# will be used for restful authentication
auth = HTTPBasicAuth()


def _get_item_or_404(user: User, uuid: str) -> Contact:
    """
    Helper function that returns a Contact based on the user and the
    exposed ID
    """
    item = Contact.query.filter_by(user=user, uuid=uuid).scalar()
    if not item:
        abort(404)
    return item


# following function is a basic method for handling authentication.
# it is used for RESTful services and tests if the user provides a password
# that, when hashed, matches the hash of a previously provided password
# users can POST to the /contacts/api/v1.0/users endpoint to create a new user

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
@main.route('/contacts/', methods=['GET'])
@auth.login_required
def index():
    """ index is the home page of the Todo Application """
    return render_template('index.html')


# These are the RESTful services (GET, PUT, POST, DELETE)
@main.route('/contacts/api/v1.0/user/create', methods=['POST'])
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


@main.route('/contacts/api/v1.0/contacts', methods=['GET'])
@auth.login_required
def get_contacts():
    """RESTful getting all contacts"""
    contacts = Contact.query.filter_by(user=g.user).all()
    return jsonify({'contacts': [item.to_json() for item in contacts]}), 200


@main.route('/contacts/api/v1.0/contact/<string:uuid>', methods=['GET'])
@auth.login_required
def get_contact(uuid):
    """RESTful getting a contact"""
    item = _get_item_or_404(g.user, uuid)
    return jsonify(item.to_json()), 200


@main.route('/contacts/api/v1.0/contact/create', methods=['POST'])
@auth.login_required
def create_contact():
    """RESTful creating a contact"""
    if not request.json:
        abort(400)
    contact = Contact.from_json(request.json)
    contact.user = g.user
    db.session.add(contact)
    db.session.commit()
    return jsonify(contact.to_json()), 201


@main.route('/contacts/api/v1.0/contact/update/<string:uuid>', methods=['PUT'])
@auth.login_required
def update_contact(uuid):
    """RESTful updating a contact"""
    if not request.json:
        abort(400)
    item = _get_item_or_404(g.user, uuid)
    item.name = request.json.get('name', item.name)
    item.email = request.json.get('email', item.email)
    item.address = request.json('address', item.address)
    item.favorite = request.json.get('favorite', item.favorite)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_json()), 200


@main.route('/contacts/api/v1.0/contact/delete/<string:uuid>', methods=['DELETE'])
@auth.login_required
def delete_contact(uuid):
    """RESTFUL deleting a contact"""
    if not request.method == 'DELETE':
        abort(400)
    item = _get_item_or_404(g.user, uuid)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'result': 'Contact deleted.'}), 200
