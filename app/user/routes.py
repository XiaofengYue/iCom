from flask import Blueprint, jsonify, request
from app import db
from app.user.forms import User

users = Blueprint('users', __name__)


@users.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    # print([user.to_dict() for user in users])
    return jsonify({'users': [user.to_dict() for user in users]})


@users.route('/api/users', methods=['POST'])
def add_user():
    p_id = request.form.get('id', None)
    p_username = request.form.get('username', None)
    p_email = request.form.get('email', None)
    p_password = request.form.get('password', None)
    new_user = User(id=p_id, username=p_username, email=p_email, password=p_password)
    # db.session.add(new_user)
    # db.session.commit()
    print(request.form)
    users = User.query.all()
    # print([user.to_dict() for user in users])
    return jsonify({'users': [user.to_dict() for user in users]})
