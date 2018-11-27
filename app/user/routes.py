from flask import Blueprint, jsonify, request
from app import db
from app.user.forms import User
import json

users = Blueprint('users', __name__)

# 返回


def return_json(code=200, msg='成功', data=None):
    return jsonify({'code': code, 'msg': msg, 'data': data})
# 注册


@users.route('/api/users/register', methods=['POST'])
def add_user():
    try:
        p_num = int(request.json.get("user_num"))
        p_pwd = request.json.get("user_pwd")
        if User.query.filter(User.user_num == p_num).all():
            return return_json(code=1, msg='账号已被注册')
        new_user = User(user_num=p_num, user_roleid=1)
        new_user.hash_password(p_pwd)
        db.session.add(new_user)
        db.session.commit()
        return return_json()
    except Exception:
        return return_json(code=0, msg='账号密码格式错误')

        # 登录


@users.route('/api/users/login', methods=['POST'])
def login():
    try:
        p_num = int(request.json.get("user_num"))
        p_pwd = request.json.get("user_pwd")
        user = User.query.filter(User.user_num == p_num).all()
        if user:
            user = user[0]
            if user.verify_password(p_pwd):
                return return_json(data='token')
            else:
                return return_json(code=2, msg='账号密码错误')
        else:
            return return_json(code=1, msg='账号尚未注册')
    except Exception:
        return return_json(code=0, msg='账号格式错误')


# 获得信息


@users.route('/api/users/message', methods=['POST'])
def get_usermsg():
    try:
        p_num = int(request.json.get("user_num"))
        user = User.query.filter(User.user_num == p_num).all()
        if user:
            user = user[0].to_dict()
            return return_json(data=user)
        else:
            return return_json(code=0, msg='查询失败')
    except Exception:
        return return_json(code=0, msg='账号格式错误')
# 更改信息


@users.route('/api/users/update', methods=['POST'])
def update_user():
    try:
        p_num = int(request.json.get("user_num"))
        user = User.query.filter(User.user_num == p_num).all()
        if user:
            user = user[0]
            user.user_name = request.json.get("user_name", user.user_name)
            user.user_sex = request.json.get("user_sex", user.user_sex)
            user.user_birthday = request.json.get("user_birthday", user.user_birthday)
            user.user_interest = request.json.get("user_interest", user.user_interest)
            user.user_headimage = request.json.get("user_headimage", user.user_headimage)
            db.session.commit()
            return return_json()
        else:
            return return_json(code=0, msg='无此用户')
    except Exception:
        return return_json(code=0, msg='无此用户')
