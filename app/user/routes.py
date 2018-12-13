from flask import Blueprint, jsonify, request, g
from app import db, auth
from app.user.forms import User
import base64

users = Blueprint('users', __name__)


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    print('用户鉴权的用户名或token:' + str(username_or_token))
    print(password)
    if not username_or_token:
        return False
    user = User.verify_auth_token(username_or_token)
    if not user:
        return False
    g.user = user
    return True


def return_json(code=200, msg='成功', data=None):
    return jsonify({'code': code, 'msg': msg, 'data': data})


'''
@Method:    注册
@Parameter: 1>>user_num 2>>user_pwd
@Return:
'''


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
        return return_json(code=0, msg='请求参数错误')


'''
@Method:    修改密码
@Parameter: 1>>user_pwd 2>>new_pwd
@Return:
'''


@users.route('/api/users/updatepwd', methods=['POST'])
@auth.login_required
def update_pwd():
    print(request.headers)
    try:
        p_pwd = request.json.get("user_pwd")
        p_newpwd = request.json.get("new_pwd")
        user = g.user
        if user:
            if user.verify_password(p_pwd):
                user.hash_password(p_newpwd)
                db.session.commit()
                return return_json()
            else:
                return return_json(code=2, msg='原密码错误')
        else:
            return return_json(code=1, msg='此用户不存在')
    except Exception:
        return return_json(code=0, msg='请求参数错误')


'''
@Method:    登录
@Parameter: 1>>user_num 2>>user_pwd
@Return:    token
'''


@users.route('/api/users/login', methods=['POST'])
def login():
    try:
        p_num = int(request.json.get("user_num"))
        p_pwd = request.json.get("user_pwd")
        user = User.query.filter(User.user_num == p_num).all()
        if user:
            user = user[0]
            if user.verify_password(p_pwd):
                g.user = user
                token = g.user.generate_auth_token()
                print('登录返回的token' + token.decode('ascii'))
                return return_json(data=[{'token:': token.decode('ascii')}])
            else:
                return return_json(code=2, msg='账号密码错误')
        else:
            return return_json(code=1, msg='账号尚未注册')
    except Exception:
        return return_json(code=0, msg='请求参数错误')


'''
@Method:    获得用户资料
@Parameter: user_num
@Return:    User
'''


@users.route('/api/users/message', methods=['POST'])
def get_usermsg():
    try:
        user_num = int(request.json.get("user_num"))
        user = User.query.filter(User.user_num == user_num).first()
        if user:
            return return_json(data=user.to_dict())
        else:
            return return_json(code=1, msg='查询失败')
    except Exception as e:
        raise e
        return return_json(code=0, msg='请求参数错误')


'''
@Method:    更新用户资料
@Parameter: NUll
@Return:
'''


@users.route('/api/users/update', methods=['POST'])
@auth.login_required
def update_user():
    try:
        user = g.user
        if user:
            user.user_name = request.json.get("user_name", user.user_name)
            user.user_sex = request.json.get("user_sex", user.user_sex)
            user.user_birthday = request.json.get("user_birthday", user.user_birthday)
            user.user_interest = request.json.get("user_interest", user.user_interest)

            user_headimage = request.json.get("user_headimage")
            if user_headimage:
                print('有图片上传')
                img = base64.b64decode(user_headimage)
                path = '/home/yxf/myproject/flask_demo/flaskblog/static/iCom_images/' + str(user.user_num) + '.jpg'
                with open(path, 'wb') as f:
                    f.write(img)
                    print('写入成功')
                user.user_headimage = 'http://www.pipicat.top/static/iCom_images/' + str(user.user_num) + '.jpg'
            db.session.commit()
            return return_json()
        else:
            return return_json(code=1, msg='无此用户')
    except Exception as e:
        raise e
        return return_json(code=0, msg='请求参数错误')
