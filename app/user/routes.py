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
    p_id = request.form.get("id", None)
    p_username = request.form.get("username", None)
    p_email = request.form.get("email", None)
    p_password = request.form.get("password", None)
    new_user = User(id=p_id, username=p_username, email=p_email, password=p_password)
    print(new_user.to_dict())
    db.session.add(new_user)
    db.session.commit()
    users = User.query.all()
    # print([user.to_dict() for user in users])
    return jsonify({'users': [user.to_dict() for user in users]})


# 返回
def return_json(code=200, msg='成功', data=None):
    return jsonify({'code': code, 'msg': msg, 'status': data})
# 注册


@users.route('/api/users/register', methods=['POST'])
def add_user():
    p_num = request.form.get("user_num")
    p_pwd = request.form.get("user_pwd")
    if User.query.filter("user_num"=p_num).all():
        return return_json(code=1, msg='账号已被注册')
    return return_json()


@users.route('/api/users/login', methods=['POST'])
def login():
    p_num = request.form.get("user_num")
    p_pwd = request.form.get("user_pwd")
    if User.query.filter(user_num=p_num).all():
        if User.query.filter(user_num=p_num, "user_pwd"=p_pwd).all():
            return return_json(data='token')
        else:
            return return_json(code=2, msg='账号密码错误')
    else:
        return return_json(code=1, msg='账号尚未注册')


@users.route('/api/users/message', methods=['POST'])
def get_usermsg():
    p_num = request.form.get("user_num")
    user = User.query.filter(user_num=p_num).all()
    if user:
        user = user[0].to_dict()
        return return_json(data=user)
    else:
        return return_json(code=0, msg='查询失败')
