from flask import Blueprint, jsonify, request
from app import db
from app.focus.forms import Focus
from app.user.forms import User
from sqlalchemy import and_

focus = Blueprint('focus', __name__)


def return_json(code=200, msg='成功', data=None):
    return jsonify({'code': code, 'msg': msg, 'data': data})

# 查


@focus.route('/api/focus/bypage', methods=['POST'])
def get_focus():
    try:
        p_page = int(request.json.get("page"))
        p_pageSize = int(request.json.get("pageSize"))
        p_master = int(request.json.get("master"))
        all_stars = User.query.filter(User.user_num == Focus.foc_star).join(Focus, Focus.foc_master == p_master).order_by(Focus.foc_id.desc()).limit(p_pageSize).offset((p_page - 1) * p_pageSize).all()
        return return_json(data=[star.to_dict() for star in all_stars])
    except Exception:
        return return_json(code=0, msg='参数错误')


# 增加
@focus.route('/api/focus/add', methods=['POST'])
def add_focus():
    try:
        p_master = int(request.json.get("master"))
        p_star = int(request.json.get("star"))
        if p_master == p_star:
            return return_json(code=2, msg='不能关注自己')
        else:
            all_focus = Focus.query.filter(and_(Focus.foc_master == p_master, Focus.foc_star == p_star)).all()
            if all_focus:
                return return_json(code=1, msg='已经关注过')
            else:
                new_focus = Focus(foc_master=p_master, foc_star=p_star)
                db.session.add(new_focus)
                db.session.commit()
                return return_json()
    except Exception:
        return return_json(code=0, msg='参数错误')


# 删除
@focus.route('/api/focus/delete', methods=['POST'])
def delete_focus():
    try:
        p_master = int(request.json.get("master"))
        p_star = int(request.json.get("star"))
        all_focus = Focus.query.filter(and_(Focus.foc_master == p_master, Focus.foc_star == p_star)).first()
        if all_focus:
            db.session.delete(all_focus)
            db.session.commit()
            return return_json()
        else:
            return return_json(code=1, msg='尚未关注')
    except Exception:
        return return_json(code=0, msg='参数错误')
