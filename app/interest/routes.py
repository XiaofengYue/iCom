from flask import Blueprint, jsonify, request
from app import db
from app.interest.forms import Interest
from app.user.forms import User
from sqlalchemy import and_


interests = Blueprint('interests', __name__)


def return_json(code=200, msg='成功', data=None):
    return jsonify({'code': code, 'msg': msg, 'data': data})

# 查


@interests.route('/api/interests/bypage', methods=['POST'])
def get_focus():
    try:
        p_page = int(request.json.get("page"))
        p_pageSize = int(request.json.get("pageSize"))
        p_usernum = int(request.json.get("usernum"))
        all_interests = Interest.query.filter(Interest.int_usernum == p_usernum).order_by(Interest.int_id.desc()).limit(p_pageSize).offset((p_page - 1) * p_pageSize).all()
        all_interests = [interest.int_typename for interest in all_interests]
        # user = User.query.filter(User.user_num == p_usernum).first()
        # user.user_interest = ','.join(all_interests)
        return return_json(data=all_interests)
    except Exception:
        return return_json(code=0, msg='参数错误')


# 增加
@interests.route('/api/interests/add', methods=['POST'])
def add_focus():
    try:
        p_usernum = int(request.json.get("usernum"))
        p_typename = request.json.get("typename")
        if not Interest.query.filter(and_(Interest.int_usernum == p_usernum, Interest.int_typename == p_typename)).all():
            new_interest = Interest(int_usernum=p_usernum, int_typename=p_typename)
            db.session.add(new_interest)
            user = User.query.filter(User.user_num == p_usernum).first()
            all_interests = Interest.query.filter(Interest.int_usernum == p_usernum).order_by(Interest.int_id.desc()).all()
            all_interests = [interest.int_typename for interest in all_interests]
            all_interests.append(p_typename)
            user.user_interest = ','.join(all_interests)
            db.session.commit()
            return return_json()
        else:
            return return_json(code=1, msg='你已经添加过')
    except Exception:
        return return_json(code=0, msg='参数错误')


# 删除
@interests.route('/api/interests/delete', methods=['POST'])
def delete_focus():
    try:
        p_usernum = int(request.json.get("usernum"))
        p_typename = request.json.get("typename")
        old_interst = Interest.query.filter(and_(Interest.int_usernum == p_usernum, Interest.int_typename == p_typename)).first()
        if old_interst:

            all_interests = Interest.query.filter(Interest.int_usernum == p_usernum).order_by(Interest.int_id.desc()).all()
            all_interests = [interest.int_typename for interest in all_interests]
            all_interests.remove(p_typename)
            user = User.query.filter(User.user_num == p_usernum).first()
            user.user_interest = ','.join(all_interests)
            db.session.delete(old_interst)
            db.session.commit()
            return return_json()
        else:
            return return_json(code=1, msg='未加入兴趣')
    except Exception as e:
        raise e
        return return_json(code=0, msg='参数错误')
