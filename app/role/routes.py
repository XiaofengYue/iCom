from flask import Blueprint, jsonify, request
from app import db
from app.role.forms import Role

roles = Blueprint('roles', __name__)

# 返回


def return_json(code=0, msg='成功', data=None):
    return jsonify({'code': code, 'msg': msg, 'data': data})

# 查


@roles.route('/api/roles', methods=['GET'])
def get_roles():
    roles = Role.query.all()
    return return_json(data=[role.to_dict() for role in roles])

# 增


@roles.route('/api/roles', methods=['POST'])
def add_roles():
    p_id = request.form.get("role_id", None)
    p_name = request.form.get("role_name", None)
    p_desc = request.form.get("role_p_desc", None)
    new_role = Role(role_id=p_id, role_name=p_name, role_desc=p_desc)
    db.session.add(new_role)
    db.session.commit()
    roles = Role.query.all()
    return return_json(data=[role.to_dict() for role in roles])
